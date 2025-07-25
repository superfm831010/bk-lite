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
    def create_qa_pairs(cls, qa_paris, chunk_obj, knowledge_base_id, embed_config, embed_model_name, qa_pairs_id):
        cls.delete_es_content(knowledge_base_id, qa_pairs_id)
        url = f"{settings.METIS_SERVER_URL}/api/rag/custom_content_ingest"
        kwargs = {
            "knowledge_base_id": knowledge_base_id,
            "knowledge_id": chunk_obj["knowledge_id"],
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
            "base_chunk_id": chunk_obj["chunk_id"],
            "qa_pairs_id": str(qa_pairs_id),
            "is_doc": "0",
        }

        for i in qa_paris:
            params = dict(kwargs, **{"content": i["question"]})
            params["metadata"] = json.dumps(dict(metadata, **{"qa_question": i["question"], "qa_answer": i["answer"]}))
            res = requests.post(url, headers=cls.get_chat_server_header(), data=params, verify=False).json()
            if res["status"] != "success":
                raise Exception(f"创建问答对失败: {res['message']}")
