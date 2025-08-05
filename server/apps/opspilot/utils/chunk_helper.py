import json
from typing import Any, Dict, Optional

import requests
from django.conf import settings

from apps.core.logger import opspilot_logger as logger
from apps.opspilot.utils.chat_server_helper import ChatServerHelper


class ChunkHelper(ChatServerHelper):
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
        url = f"{settings.METIS_SERVER_URL}/api/rag/list_rag_document"
        query = {
            "index_name": index_name,
            "page": page,
            "metadata_filter": metadata_filter,
            "size": page_size,
            "query": search_text,
        }
        res = cls.post_chat_server(query, url)
        if not res:
            return {"count": 0, "documents": []}
        count_res = {"count": 0}
        if get_count:
            count_url = f"{settings.METIS_SERVER_URL}/api/rag/count_index_document"
            count_res = ChatServerHelper.post_chat_server(query, count_url)
        res["count"] = count_res.get("count", 0)
        return res

    @staticmethod
    def delete_es_content(index_name, qa_pairs_id):
        url = f"{settings.METIS_SERVER_URL}/api/rag/delete_doc"
        kwargs = {"index_name": index_name, "metadata_filter": {"qa_pairs_id": str(qa_pairs_id)}}
        try:
            ChatServerHelper.post_chat_server(kwargs, url)
        except Exception as e:
            logger.exception(e)

    @classmethod
    def create_qa_pairs(cls, qa_paris, chunk_obj, index_name, embed_config, embed_model_name, qa_pairs_id):
        success_count = 0
        cls.delete_es_content(index_name, qa_pairs_id)
        url = f"{settings.METIS_SERVER_URL}/api/rag/custom_content_ingest"
        kwargs, metadata = cls.set_qa_pairs_params(embed_config, embed_model_name, index_name, qa_pairs_id, chunk_obj)
        for i in qa_paris:
            params = dict(kwargs, **{"content": i["question"]})
            params["metadata"] = json.dumps(dict(metadata, **{"qa_question": i["question"], "qa_answer": i["answer"]}))
            res = requests.post(url, headers=cls.get_chat_server_header(), data=params, verify=False).json()
            if res["status"] != "success":
                logger.exception(f"创建问答对失败: {res['message']}")
                continue
            success_count += 1
        return success_count

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
    def create_one_qa_pairs(cls, embed_config, embed_model_name, index_name, qa_pairs_id, question, answer):
        url = f"{settings.METIS_SERVER_URL}/api/rag/custom_content_ingest"
        kwargs, metadata = cls.set_qa_pairs_params(embed_config, embed_model_name, index_name, qa_pairs_id)
        metadata.update({"qa_question": question, "qa_answer": answer})
        params = dict(kwargs, **{"content": question, "metadata": json.dumps(metadata)})
        res = requests.post(url, headers=cls.get_chat_server_header(), data=params, verify=False).json()
        if res["status"] != "success":
            logger.exception(f"创建问答对失败: {res['message']}")
            return {"result": False}
        return {"result": True}

    @staticmethod
    def update_qa_pairs(index_name, chunk_id, question, answer):
        url = f"{settings.METIS_SERVER_URL}/api/rag/update_rag_document_metadata"
        kwargs = {
            "index_name": index_name,
            "metadata_filter": {"chunk_id": str(chunk_id)},
            "metadata": {"qa_question": question, "qa_answer": answer},
        }
        res = ChatServerHelper.post_chat_server(kwargs, url)
        return res
