import json
import os

import requests
import logging

logger = logging.getLogger(__name__)


def test_xinference_reranker():
    try:
        headers = {
            "accept": "application/json", "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('TEST_INFERENCE_TOKEN')}"
        }
        data = {
            "model": "bce-reranker-base_v1",
            "query": "What is the capital of France?",
            "documents": [
                "The capital of Brazil is Brasilia.",
                "The capital of France is Paris.", "Horses and cows are both animals"
            ]
        }
        response = requests.post(
            f"{os.getenv('TEST_INFERENCE_BASE_URL')}/rerank", headers=headers, json=data)
        logger.info(json.dumps(response.json(), indent=2))
    except Exception as e:
        logger.warning(f"XInference远端服务暂时不可用")
