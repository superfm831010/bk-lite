import json
import time

import requests
from celery import shared_task
from django.conf import settings
from tqdm import tqdm

from apps.core.logger import opspilot_logger as logger
from apps.opspilot.knowledge_mgmt.models import KnowledgeGraph, QAPairs
from apps.opspilot.knowledge_mgmt.models.knowledge_document import DocumentStatus
from apps.opspilot.knowledge_mgmt.models.knowledge_task import KnowledgeTask
from apps.opspilot.knowledge_mgmt.services.knowledge_search_service import KnowledgeSearchService
from apps.opspilot.model_provider_mgmt.models import LLMModel
from apps.opspilot.models import FileKnowledge, KnowledgeBase, KnowledgeDocument, ManualKnowledge, WebPageKnowledge
from apps.opspilot.utils.chat_server_helper import ChatServerHelper
from apps.opspilot.utils.chunk_helper import ChunkHelper
from apps.opspilot.utils.graph_utils import GraphUtils


@shared_task
def general_embed(knowledge_document_id_list, username, domain="domain.com"):
    logger.info(f"general_embed: {knowledge_document_id_list}")
    document_list = KnowledgeDocument.objects.filter(id__in=knowledge_document_id_list)
    general_embed_by_document_list(document_list, username=username, domain=domain)
    logger.info(f"knowledge training finished: {knowledge_document_id_list}")


@shared_task
def retrain_all(knowledge_base_id, username, domain="domain.com"):
    logger.info("Start retraining")
    document_list = KnowledgeDocument.objects.filter(knowledge_base_id=knowledge_base_id)
    document_list.update(train_status=DocumentStatus.CHUNKING)
    general_embed_by_document_list(document_list, username=username, domain=domain)


def general_embed_by_document_list(document_list, is_show=False, username="", domain="domain.com"):
    if is_show:
        res, remote_docs = invoke_one_document(document_list[0], is_show)
        docs = [i["page_content"] for i in remote_docs][:10]
        return docs
    knowledge_base_id = document_list[0].knowledge_base_id
    task_obj = KnowledgeTask.objects.create(
        created_by=username,
        domain=domain,
        knowledge_base_id=knowledge_base_id,
        task_name=document_list[0].name,
        knowledge_ids=[doc.id for doc in document_list],
        train_progress=0,
    )
    train_progress = round(float(1 / len(task_obj.knowledge_ids)) * 100, 2)
    for index, document in tqdm(enumerate(document_list)):
        try:
            invoke_document_to_es(document=document)
        except Exception as e:
            logger.exception(e)
        task_progress = task_obj.train_progress + train_progress
        task_obj.train_progress = round(task_progress, 2)
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
                "azure_api_key": knowledge_document.ocr_model.ocr_config["api_key"] or " ",
                "azure_endpoint": knowledge_document.ocr_model.ocr_config["base_url"],
            }
        elif knowledge_document.ocr_model.name == "OlmOCR":
            ocr_config = {
                "ocr_type": "olm_ocr",
                "olm_base_url": knowledge_document.ocr_model.ocr_config["base_url"],
                "olm_api_key": knowledge_document.ocr_model.ocr_config["api_key"] or " ",
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
        "embed_model_api_key": embed_config.get("api_key", "") or " ",
        "embed_model_name": embed_config.get("model", embed_model_name),
        "chunk_mode": knowledge_document.chunk_type,
        "chunk_size": knowledge_document.general_parse_chunk_size,
        "chunk_overlap": knowledge_document.general_parse_chunk_overlap,
        "load_mode": knowledge_document.mode,
        "semantic_chunk_model_base_url": [semantic_embed_config.get("base_url", "")]
        if semantic_embed_config.get("base_url", "")
        else [],
        "semantic_chunk_model_api_key": semantic_embed_config.get("api_key", "") or " ",
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
        logger.error(f"Web page knowledge {web_page_knowledge_id} not found.")
        return
    document_list = [web_page.knowledge_document]
    web_page.knowledge_document.train_status = DocumentStatus.CHUNKING
    web_page.knowledge_document.save()
    general_embed_by_document_list(
        document_list, username=web_page.knowledge_document.created_by, domain=web_page.knowledge_document.domain
    )


@shared_task
def create_qa_pairs(qa_pairs_id_list, llm_model_id, qa_count, knowledge_base_id):
    qa_pairs_list = QAPairs.objects.filter(id__in=qa_pairs_id_list)
    if not qa_pairs_list:
        logger.info(f"QAPairs with ID {qa_pairs_id_list} not found.")
        return
    knowledge_base = KnowledgeBase.objects.filter(id=knowledge_base_id).first()
    if not knowledge_base:
        logger.error(f"KnowledgeBase with ID {knowledge_base_id} not found.")
        return
    llm_model = LLMModel.objects.filter(id=llm_model_id).first()
    if not llm_model:
        logger.error(f"LLMModel with ID {llm_model_id} not found.")
        return
    username = qa_pairs_list[0].created_by
    task_obj = KnowledgeTask.objects.create(
        created_by=username,
        domain=qa_pairs_list[0].domain,
        knowledge_base_id=knowledge_base_id,
        task_name=qa_pairs_list[0].name,
        knowledge_ids=[doc for doc in qa_pairs_id_list],
        train_progress=0,
    )
    train_progress = round(float(1 / len(task_obj.knowledge_ids)) * 100, 2)

    url = f"{settings.METIS_SERVER_URL}/api/rag/qa_pair_generate"
    es_index = knowledge_base.knowledge_index_name()
    embed_config = knowledge_base.embed_model.decrypted_embed_config
    embed_model_name = knowledge_base.embed_model.name
    openai_api_base = llm_model.decrypted_llm_config["openai_base_url"]
    openai_api_key = llm_model.decrypted_llm_config["openai_api_key"]
    model = llm_model.decrypted_llm_config["model"]
    try:
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
                ChunkHelper.create_qa_pairs(
                    res["message"], i, es_index, embed_config, embed_model_name, qa_pairs_obj.id
                )
            task_progress = task_obj.train_progress + train_progress
            task_obj.train_progress = round(task_progress, 2)
            task_obj.save()
    except Exception as e:
        logger.exception(f"Error creating QA pairs: {str(e)}")
    task_obj.delete()


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


@shared_task
def rebuild_graph_community_by_instance(instance_id):
    graph_obj = KnowledgeGraph.objects.get(id=instance_id)
    res = GraphUtils.rebuild_graph_community(graph_obj)
    if not res["result"]:
        logger.error("Failed to rebuild graph community: {}".format(res["message"]))
    logger.info("Graph community rebuild completed for instance ID: {}".format(instance_id))


@shared_task
def create_graph(instance_id):
    logger.info("Start creating graph for instance ID: {}".format(instance_id))
    instance = KnowledgeGraph.objects.get(id=instance_id)
    res = GraphUtils.create_graph(instance)
    if not res["result"]:
        instance.delete()
        logger.error("Failed to create graph: {}".format(res["message"]))
    else:
        logger.info("Graph created completed: {}".format(instance.name))


@shared_task
def update_graph(instance_id, old_doc_list):
    logger.info("Start updating graph for instance ID: {}".format(instance_id))
    instance = KnowledgeGraph.objects.get(id=instance_id)
    res = GraphUtils.update_graph(instance, old_doc_list)
    if not res["result"]:
        logger.error("Failed to update graph: {}".format(res["message"]))
    else:
        logger.info("Graph updated completed: {}".format(instance.name))


@shared_task
def create_qa_pairs_by_json(file_data, knowledge_base_id, username, domain):
    """
    通过JSON数据批量创建问答对

    Args:
        file_data: 包含问答对数据的JSON列表，每个元素包含instruction和output字段
        knowledge_base_id: 知识库ID
        username: 创建用户名
        domain: 域名
    """
    # 获取知识库对象
    knowledge_base = KnowledgeBase.objects.filter(id=knowledge_base_id).first()
    if not knowledge_base:
        return

    # 初始化任务和问答对对象
    task_obj, qa_pairs_list = _initialize_qa_task(file_data, knowledge_base_id, username, domain)

    # 批量处理问答对
    try:
        _process_qa_pairs_batch(qa_pairs_list, file_data, knowledge_base, task_obj)
    except Exception as e:
        logger.exception(f"批量创建问答对失败: {str(e)}")

    # 清理任务对象
    task_obj.delete()
    logger.info("批量创建问答对任务完成")


def _initialize_qa_task(file_data, knowledge_base_id, username, domain):
    """初始化任务和问答对对象"""
    task_name = list(file_data.keys())[0]
    qa_pairs_list = []
    qa_pairs_id_list = []

    # 创建问答对对象
    for qa_name in file_data.keys():
        qa_pairs = create_qa_pairs_task(knowledge_base_id, qa_name)
        if qa_pairs.id not in qa_pairs_id_list:
            qa_pairs_list.append(qa_pairs)
            qa_pairs_id_list.append(qa_pairs.id)

    # 创建任务跟踪对象
    task_obj = KnowledgeTask.objects.create(
        created_by=username,
        domain=domain,
        knowledge_base_id=knowledge_base_id,
        task_name=task_name,
        knowledge_ids=qa_pairs_id_list,
        train_progress=0,
    )

    return task_obj, qa_pairs_list


def _process_qa_pairs_batch(qa_pairs_list, file_data, knowledge_base, task_obj):
    """批量处理问答对数据"""
    url = f"{settings.METIS_SERVER_URL}/api/rag/custom_content_ingest"
    headers = ChatServerHelper.get_chat_server_header()
    kwargs = set_import_kwargs(knowledge_base)
    train_progress = round(float(1 / len(qa_pairs_list)) * 100, 2)

    for qa_pairs in qa_pairs_list:
        qa_json = file_data[qa_pairs.name]
        success_count = _process_single_qa_pairs(qa_pairs, qa_json, kwargs, url, headers)

        # 更新问答对数量和任务进度
        qa_pairs.qa_count += success_count
        qa_pairs.save()
        task_progress = task_obj.train_progress + train_progress
        task_obj.train_progress = round(task_progress, 2)
        task_obj.save()

        logger.info(f"批量创建问答对完成: {qa_pairs.name}, 总数: {len(qa_json)}, 成功: {success_count}")


def _process_single_qa_pairs(qa_pairs, qa_json, kwargs, url, headers):
    """处理单个问答对集合"""
    metadata = {
        "enabled": True,
        "base_chunk_id": "",
        "qa_pairs_id": str(qa_pairs.id),
        "is_doc": "0",
    }

    success_count = 0
    error_count = 0

    logger.info(f"开始处理问答对数据: {qa_pairs.name}")
    for index, qa_item in enumerate(tqdm(qa_json)):
        result = _create_single_qa_item(qa_item, index, kwargs, metadata, url, headers)
        if result is None:
            continue
        elif result:
            success_count += 1
        else:
            error_count += 1
        # 每10个记录输出一次进度日志
        if (index + 1) % 10 == 0:
            logger.info(f"已处理 {index + 1}/{len(qa_json)} 个问答对，成功: {success_count}, 失败: {error_count}")

    return success_count


def _create_single_qa_item(qa_item, index, kwargs, metadata, url, headers):
    """创建单个问答项"""
    if not qa_item["instruction"]:
        logger.warning(f"跳过空instruction，索引: {index}")
        return None

    # 构建请求参数
    params = dict(kwargs, **{"content": qa_item["instruction"]})
    params["metadata"] = json.dumps(
        dict(metadata, **{"qa_question": qa_item["instruction"], "qa_answer": qa_item["output"]})
    )

    # 尝试创建问答对，带重试机制
    return _send_qa_request_with_retry(params, url, headers, index)


def _send_qa_request_with_retry(params, url, headers, index):
    """发送问答对创建请求，带重试机制"""
    try:
        res = requests.post(url, headers=headers, data=params, verify=False).json()
        if res.get("status") != "success":
            raise Exception(f"创建问答对失败: {res['message']}")
    except Exception as e:
        logger.warning(f"第一次请求失败，准备重试。索引: {index}, 错误: {str(e)}")
        # 重试机制：等待5秒后重试
        time.sleep(5)
        try:
            res = requests.post(url, headers=headers, data=params, verify=False).json()
            if res.get("status") != "success":
                raise Exception(f"重试后仍然失败: {res['message']}")
            logger.info(f"重试成功，索引: {index}")
        except Exception as retry_e:
            logger.error(f"创建问答对失败，索引: {index}, 错误: {str(retry_e)}")
            if hasattr(retry_e, "response"):
                logger.error(f"响应内容: {retry_e.response}")
            return False
    return True


def create_qa_pairs_task(knowledge_base_id, qa_name):
    # 创建或获取问答对对象
    qa_pairs, created = QAPairs.objects.get_or_create(
        name=qa_name,
        knowledge_base_id=knowledge_base_id,
        document_id=0,
    )
    logger.info(f"问答对对象{'创建' if created else '获取'}成功: {qa_pairs.name}")
    return qa_pairs


def set_import_kwargs(knowledge_base):
    embed_config = knowledge_base.embed_model.decrypted_embed_config
    embed_model_name = knowledge_base.embed_model.name
    kwargs = {
        "knowledge_base_id": knowledge_base.knowledge_index_name(),
        "knowledge_id": "0",
        "embed_model_base_url": embed_config.get("base_url", ""),
        "embed_model_api_key": embed_config.get("api_key", "") or " ",
        "embed_model_name": embed_config.get("model", embed_model_name),
        "chunk_mode": "full",
        "chunk_size": 9999,
        "chunk_overlap": 128,
        "load_mode": "full",
        "semantic_chunk_model_base_url": [],
        "semantic_chunk_model_api_key": " ",
        "semantic_chunk_model": "",
        "preview": "false",
    }

    return kwargs
