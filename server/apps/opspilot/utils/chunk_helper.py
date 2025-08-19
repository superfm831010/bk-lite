import json
import os
from typing import Any, Dict, Optional

import requests
from django.conf import settings

from apps.core.logger import opspilot_logger as logger
from apps.opspilot.utils.chat_server_helper import ChatServerHelper


class ChunkHelper(ChatServerHelper):
    list_url = f"{settings.METIS_SERVER_URL}/api/rag/list_rag_document"
    generate_url = f"{settings.METIS_SERVER_URL}/api/rag/qa_pair_generate"
    del_url = f"{settings.METIS_SERVER_URL}/api/rag/delete_doc"
    create_url = f"{settings.METIS_SERVER_URL}/api/rag/custom_content_ingest"
    update_url = f"{settings.METIS_SERVER_URL}/api/rag/update_rag_document_metadata"

    @classmethod
    def create_qa_pairs_by_content(
        cls,
        content_list,
        embed_config,
        embed_model_name,
        es_index,
        model,
        openai_api_base,
        openai_api_key,
        qa_count,
        qa_pairs_obj,
        is_delete=True,
        task_obj=None,
    ):
        success_count = 0
        for i in content_list:
            params = {
                "size": qa_count,
                "content": i["content"],
                "openai_api_base": openai_api_base,
                "openai_api_key": openai_api_key,
                "model": model,
                "extra_prompt": "do occaecat",
            }
            res = ChatServerHelper.post_chat_server(params, cls.generate_url)
            if res.get("status", "fail") != "success":
                logger.error(f"Failed to create QA pairs for Chunk ID {i['chunk_id']}.")
                if task_obj:
                    task_obj.completed_count += 1
                    task_obj.save()
                continue
            try:
                chunk_success_count = cls.create_qa_pairs(
                    res["message"], i, es_index, embed_config, embed_model_name, qa_pairs_obj.id, is_delete
                )
                success_count += chunk_success_count
                res = cls.update_document_qa_pairs_count(es_index, chunk_success_count, i["chunk_id"])
                if not res:
                    logger.error(f"Failed to update document QA pairs count for chunk_id ID: {i['chunk_id']}")
            except Exception as e:
                logger.exception(e)
            if task_obj:
                task_obj.completed_count += 1
                task_obj.save()
        return success_count

    @classmethod
    def get_document_es_chunk(
        cls,
        index_name,
        page: int = 1,
        page_size: int = 0,
        search_text: str = "",
        metadata_filter: Optional[Dict[str, Any]] = None,
        get_count: bool = True,
    ) -> Dict[str, Any]:
        if not metadata_filter:
            metadata_filter = {}
        query = {
            "index_name": index_name,
            "page": page,
            "metadata_filter": metadata_filter,
            "size": page_size,
            "query": search_text,
            "sort_field": "created_time",
            "sort_order": "asc",
        }
        res = cls.post_chat_server(query, cls.list_url)
        if not res:
            return {"count": 0, "documents": []}
        count_res = {"count": 0}
        if get_count:
            count_url = f"{settings.METIS_SERVER_URL}/api/rag/count_index_document"
            count_res = ChatServerHelper.post_chat_server(query, count_url)
        res["count"] = count_res.get("count", 0)
        return res

    @classmethod
    def delete_es_content(cls, index_name, qa_pairs_id):
        kwargs = {"index_name": index_name, "metadata_filter": {"qa_pairs_id": str(qa_pairs_id)}}
        try:
            ChatServerHelper.post_chat_server(kwargs, cls.del_url)
        except Exception as e:
            logger.exception(e)

    @classmethod
    def delete_chunk(cls, index_name, chunk_id, is_base=False):
        if is_base:
            kwargs = {"index_name": index_name, "metadata_filter": {"base_chunk_id": str(chunk_id)}}
        else:
            kwargs = {"index_name": index_name, "metadata_filter": {"chunk_id": str(chunk_id)}}
        try:
            ChatServerHelper.post_chat_server(kwargs, cls.del_url)
        except Exception as e:
            logger.exception(e)
            return {"result": False}
        return {"result": True}

    @classmethod
    def delete_chunk_relation(cls, index_name, chunk_id):
        kwargs = {
            "index_name": index_name,
            "metadata_filter": {"base_chunk_id": str(chunk_id)},
            "metadata": {"base_chunk_id": ""},
        }
        try:
            ChatServerHelper.post_chat_server(kwargs, cls.update_url)
        except Exception as e:
            logger.exception(e)
            return {"result": False}
        return {"result": True}

    @classmethod
    def create_qa_pairs(
        cls, qa_paris, chunk_obj, index_name, embed_config, embed_model_name, qa_pairs_id, is_delete=True
    ):
        success_count = 0
        if is_delete:
            cls.delete_es_content(index_name, qa_pairs_id)
        kwargs, metadata = cls.set_qa_pairs_params(embed_config, embed_model_name, index_name, qa_pairs_id, chunk_obj)
        headers = cls.get_chat_server_header()
        # SSL验证配置 - 从环境变量读取
        ssl_verify = os.getenv("METIS_SSL_VERIFY", "false").lower() == "true"
        for i in qa_paris:
            params = dict(kwargs, **{"content": i["question"]})
            params["metadata"] = json.dumps(dict(metadata, **{"qa_question": i["question"], "qa_answer": i["answer"]}))
            response = requests.post(cls.create_url, headers=headers, data=params, verify=ssl_verify)
            res = response.json()
            if res.get("status", "fail") != "success":
                logger.exception(f"创建问答对失败: {res.get('message', '')}")
                continue
            success_count += 1
        return success_count

    @classmethod
    def update_document_qa_pairs_count(cls, es_index, qa_count, chunk_id):
        if not qa_count:
            return {}
        current_count = cls.get_chunk_qa_count(es_index, chunk_id)
        qa_count += current_count
        kwargs = {
            "index_name": es_index,
            "metadata_filter": {"chunk_id": str(chunk_id), "is_doc": "1"},
            "metadata": {"qa_count": qa_count},
        }
        res = ChatServerHelper.post_chat_server(kwargs, cls.update_url)
        return res

    @classmethod
    def get_chunk_qa_count(cls, es_index, chunk_id):
        obj = cls.get_document_es_chunk(
            es_index, metadata_filter={"chunk_id": str(chunk_id), "is_doc": "1"}, get_count=False
        )
        if obj.get("document", []):
            return obj["document"][0].get("metadata", {}).get("qa_count", 0)
        return 0

    @classmethod
    def set_qa_pairs_params(cls, embed_config, embed_model_name, index_name, qa_pairs_id, chunk_obj=None):
        if chunk_obj is None:
            chunk_obj = {}
        kwargs = {
            "knowledge_base_id": index_name,
            "knowledge_id": chunk_obj.get("knowledge_id", "0"),
            "embed_model_base_url": embed_config.get("base_url", ""),
            "embed_model_api_key": embed_config.get("api_key", "") or " ",
            "embed_model_name": embed_config.get("model", embed_model_name),
            "chunk_mode": "full",
            "chunk_size": 9999,
            "chunk_overlap": 128,
            "load_mode": "full",
            "semantic_chunk_model_base_url": [],
            "semantic_chunk_model_api_key": "",
            "semantic_chunk_model": "",
            "preview": "false",
        }
        metadata = {
            "enabled": True,
            "base_chunk_id": chunk_obj.get("chunk_id", ""),
            "qa_pairs_id": str(qa_pairs_id),
            "is_doc": "0",
        }
        return kwargs, metadata

    @classmethod
    def create_one_qa_pairs(
        cls, embed_config, embed_model_name, index_name, qa_pairs_id, knowledge_id, question, answer
    ):
        chunk_obj = {"knowledge_id": knowledge_id}
        kwargs, metadata = cls.set_qa_pairs_params(embed_config, embed_model_name, index_name, qa_pairs_id, chunk_obj)
        metadata.update({"qa_question": question, "qa_answer": answer})
        params = dict(kwargs, **{"content": question, "metadata": json.dumps(metadata)})
        # SSL验证配置 - 从环境变量读取
        ssl_verify = os.getenv("METIS_SSL_VERIFY", "false").lower() == "true"
        res = requests.post(cls.create_url, headers=cls.get_chat_server_header(), data=params, verify=ssl_verify).json()
        if res.get("status", "fail") != "success":
            logger.exception(f"创建问答对失败: {res.get('message', '')}")
            return {"result": False}
        return {"result": True}

    @classmethod
    def update_qa_pairs(cls, index_name, chunk_id, question, answer):
        kwargs = {
            "index_name": index_name,
            "metadata_filter": {"chunk_id": str(chunk_id)},
            "metadata": {"qa_question": question, "qa_answer": answer},
        }
        res = ChatServerHelper.post_chat_server(kwargs, cls.update_url)
        return res
