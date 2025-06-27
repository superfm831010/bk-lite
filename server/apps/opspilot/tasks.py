import json

import requests
from celery import shared_task
from django.conf import settings
from tqdm import tqdm

from apps.core.logger import opspilot_logger as logger
from apps.opspilot.knowledge_mgmt.models import QAPairs
from apps.opspilot.knowledge_mgmt.models.knowledge_document import DocumentStatus
from apps.opspilot.knowledge_mgmt.models.knowledge_task import KnowledgeTask
from apps.opspilot.knowledge_mgmt.services.knowledge_search_service import KnowledgeSearchService
from apps.opspilot.model_provider_mgmt.models import LLMModel
from apps.opspilot.models import FileKnowledge, KnowledgeBase, KnowledgeDocument, ManualKnowledge, WebPageKnowledge
from apps.opspilot.utils.chat_server_helper import ChatServerHelper
from apps.opspilot.utils.chunk_helper import ChunkHelper


@shared_task
def general_embed(knowledge_document_id_list, username):
    logger.info(f"general_embed: {knowledge_document_id_list}")
    document_list = KnowledgeDocument.objects.filter(id__in=knowledge_document_id_list)
    general_embed_by_document_list(document_list, username=username)
    logger.info(f"knowledge training finished: {knowledge_document_id_list}")


@shared_task
def retrain_all(knowledge_base_id, username):
    logger.info("Start retraining")
    knowledge_base = KnowledgeBase.objects.get(id=knowledge_base_id)
    knowledge_base.recreate_es_index()
    document_list = KnowledgeDocument.objects.filter(knowledge_base_id=knowledge_base_id)
    document_list.update(train_status=DocumentStatus.CHUNKING)
    general_embed_by_document_list(document_list, username=username)


def general_embed_by_document_list(document_list, is_show=False, username=""):
    if is_show:
        res, remote_docs = invoke_one_document(document_list[0], is_show)
        docs = [i["page_content"] for i in remote_docs][:10]
        return docs
    knowledge_base_id = document_list[0].knowledge_base_id
    task_obj = KnowledgeTask.objects.create(
        created_by=username,
        knowledge_base_id=knowledge_base_id,
        task_name=document_list[0].name,
        knowledge_ids=[doc.id for doc in document_list],
        train_progress=0,
    )
    train_progress = round(float(1 / len(task_obj.knowledge_ids)) * 100, 2)
    for index, document in tqdm(enumerate(document_list)):
        invoke_document_to_es(document=document)
        task_obj.train_progress += train_progress
        if index < len(document_list) - 1:
            task_obj.name = document_list[index + 1].name
        task_obj.save()
    task_obj.delete()


@shared_task
def invoke_document_to_es(document_id=0, document=None):
    if document_id:
        document = KnowledgeDocument.objects.filter(id=document_id).first()
    if not document:
        logger.error(f"document {document_id} not found")
        return
    document.train_status = DocumentStatus.TRAINING
    document.chunk_size = 0
    document.save()
    logger.info(f"document {document.name} progress: {document.train_progress}")
    KnowledgeSearchService.delete_es_content(document.knowledge_index_name(), document.id, document.name)
    res, knowledge_docs = invoke_one_document(document)
    if not res:
        document.train_status = DocumentStatus.ERROR
        document.save()
        return
    document.train_status = DocumentStatus.READY
    document.save()
    logger.info(f"document {document.name} progress: {document.train_progress}")


def invoke_one_document(document, is_show=False):
    source_invoke_format_map = {
        "file": format_file_invoke_kwargs,
        "manual": format_manual_invoke_kwargs,
        "web_page": format_web_page_invoke_kwargs,
    }
    remote_url_map = {
        "file": f"{settings.METIS_SERVER_URL}/api/rag/file_ingest",
        "web_page": f"{settings.METIS_SERVER_URL}/api/rag/website_ingest",
        "manual": f"{settings.METIS_SERVER_URL}/api/rag/custom_content_ingest",
    }
    knowledge_docs = []
    source_type = document.knowledge_source_type
    source_remote = remote_url_map[source_type]
    logger.info("Start handle {} knowledge: {}".format(source_type, document.name))
    form_data = format_invoke_kwargs(document, preview=is_show)
    source_data = source_invoke_format_map[source_type](document)
    res = {"status": "fail"}
    try:
        headers = ChatServerHelper.get_chat_server_header()
        if source_type == "file":
            files = source_data.pop("file")
            res = requests.post(source_remote, headers=headers, data=form_data, files=files, verify=False).json()
        else:
            form_data.update(source_data)
            res = requests.post(source_remote, headers=headers, data=form_data, verify=False).json()
        remote_docs = res.get("documents", [])
        document.chunk_size = res.get("chunks_size", 0)
        if not document.chunk_size:
            logger.error(f"获取不到文档，返回结果为： {res}")
        knowledge_docs.extend(remote_docs)
    except Exception as e:
        logger.exception(e)
    return res["status"] == "success", knowledge_docs


def format_file_invoke_kwargs(document):
    knowledge = FileKnowledge.objects.filter(knowledge_document_id=document.id).first()
    return {"file": [("file", (knowledge.file.name, knowledge.file.read(), "application/octet-stream"))]}


def format_manual_invoke_kwargs(document):
    knowledge = ManualKnowledge.objects.filter(knowledge_document_id=document.id).first()
    return {
        "content": document.name + knowledge.content,
    }


def format_web_page_invoke_kwargs(document):
    knowledge = WebPageKnowledge.objects.filter(knowledge_document_id=document.id).first()
    return {
        "url": knowledge.url,
        "max_depth": knowledge.max_depth,
    }


def format_invoke_kwargs(knowledge_document: KnowledgeDocument, preview=False):
    embed_config = {}
    embed_model_name = ""
    semantic_embed_config = {}
    semantic_embed_model_name = ""
    if knowledge_document.knowledge_base.embed_model:
        embed_config = knowledge_document.knowledge_base.embed_model.decrypted_embed_config
        embed_model_name = knowledge_document.knowledge_base.embed_model.name
    if knowledge_document.semantic_chunk_parse_embedding_model:
        semantic_embed_config = knowledge_document.semantic_chunk_parse_embedding_model.decrypted_embed_config
        semantic_embed_model_name = knowledge_document.semantic_chunk_parse_embedding_model.name
    ocr_config = {}
    if knowledge_document.enable_ocr_parse:
        if knowledge_document.ocr_model.name == "AzureOCR":
            ocr_config = {
                "ocr_type": "azure_ocr",
                "azure_api_key": knowledge_document.ocr_model.ocr_config["api_key"],
                "azure_endpoint": knowledge_document.ocr_model.ocr_config["base_url"],
            }
        elif knowledge_document.ocr_model.name == "OlmOCR":
            ocr_config = {
                "ocr_type": "olm_ocr",
                "olm_base_url": knowledge_document.ocr_model.ocr_config["base_url"],
                "olm_api_key": knowledge_document.ocr_model.ocr_config["api_key"],
                "olm_model": knowledge_document.ocr_model.name,
            }
        else:
            ocr_config = {
                "ocr_type": "pp_ocr",
            }
    kwargs = {
        "knowledge_base_id": knowledge_document.knowledge_index_name(),
        "knowledge_id": str(knowledge_document.id),
        "embed_model_base_url": embed_config.get("base_url", ""),
        "embed_model_api_key": embed_config.get("api_key", ""),
        "embed_model_name": embed_config.get("model", embed_model_name),
        "chunk_mode": knowledge_document.chunk_type,
        "chunk_size": knowledge_document.general_parse_chunk_size,
        "chunk_overlap": knowledge_document.general_parse_chunk_overlap,
        "load_mode": knowledge_document.mode,
        "semantic_chunk_model_base_url": [semantic_embed_config.get("base_url", "")]
        if semantic_embed_config.get("base_url", "")
        else [],
        "semantic_chunk_model_api_key": semantic_embed_config.get("api_key", ""),
        "semantic_chunk_model": semantic_embed_config.get("model", semantic_embed_model_name),
        "preview": "true" if preview else "false",
        "metadata": json.dumps({"enabled": True, "is_doc": "1"}),
    }
    kwargs.update(ocr_config)
    return kwargs


@shared_task
def sync_web_page_knowledge(web_page_knowledge_id):
    """
    Sync web page knowledge by ID.
    """
    web_page = WebPageKnowledge.objects.filter(id=web_page_knowledge_id).first()
    if not web_page:
        return {"result": False, "message": "Web page knowledge not found."}

    knowledge_base = web_page.knowledge_document.knowledge_base
    knowledge_base.recreate_es_index()
    document_list = [web_page.knowledge_document]
    web_page.knowledge_document.train_status = DocumentStatus.CHUNKING
    web_page.knowedge_document.save()
    general_embed_by_document_list(document_list, username=KnowledgeDocument.created_by)


@shared_task
def create_qa_pairs(qa_pairs_id_list, llm_model_id, qa_count, knowledge_base_id):
    qa_pairs_list = QAPairs.objects.filter(id__in=qa_pairs_id_list)
    if not qa_pairs_list:
        logger.info(f"QAPairs with ID {qa_pairs_id_list} not found.")
        return
    url = f"{settings.METIS_SERVER_URL}/api/rag/qa_pair_generate"
    llm_model = LLMModel.objects.filter(id=llm_model_id).first()
    if not llm_model:
        logger.error(f"LLMModel with ID {llm_model_id} not found.")
        return
    knowledge_base = KnowledgeBase.objects.filter(id=knowledge_base_id).first()
    if not knowledge_base:
        logger.error(f"KnowledgeBase with ID {knowledge_base_id} not found.")
        return
    es_index = knowledge_base.knowledge_index_name()
    embed_config = knowledge_base.embed_model.decrypted_embed_config
    embed_model_name = knowledge_base.embed_model.name
    openai_api_base = llm_model.decrypted_llm_config["openai_base_url"]
    openai_api_key = llm_model.decrypted_llm_config["openai_api_key"]
    model = llm_model.decrypted_llm_config["model"]
    for qa_pairs_obj in qa_pairs_list:
        content_list = get_qa_content(qa_pairs_obj, es_index)
        for i in content_list:
            params = {
                "size": qa_count,
                "content": i["content"],
                "openai_api_base": openai_api_base,
                "openai_api_key": openai_api_key,
                "model": model,
            }
            res = ChatServerHelper.post_chat_server(params, url)
            if res.get("status", "fail") != "success":
                logger.error(f"Failed to create QA pairs for Chunk ID {i['chunk_id']}.")
                continue
            ChunkHelper.create_qa_pairs(res["message"], i, es_index, embed_config, embed_model_name, qa_pairs_obj.id)


def get_qa_content(qa_pairs_obj: QAPairs, es_index):
    client = ChunkHelper()
    document_id = qa_pairs_obj.document_id
    res = client.get_document_es_chunk(
        es_index, 1, 10000, metadata_filter={"knowledge_id": str(document_id)}, get_count=False
    )
    if res.get("status") != "success":
        raise Exception(f"Failed to get document chunk for document ID {document_id}.")
    return_data = []
    for i in res["documents"]:
        meta_data = i.get("metadata", {})
        if not meta_data:
            continue
        return_data.append(
            {
                "chunk_id": meta_data["chunk_id"],
                "content": i["page_content"],
                "knowledge_id": meta_data["knowledge_id"],
            }
        )
    return return_data
