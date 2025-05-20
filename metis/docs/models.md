# 内置模型

## Embed

| 模型名称                  | url                                                            |
|-----------------------|----------------------------------------------------------------|
| bge-small-zh-v1.5     | local:huggingface_embedding:BAAI/bge-small-zh-v1.5             |
| bce-embedding-base_v1 | local:huggingface_embedding:maidalun1020/bce-embedding-base_v1 |

## ReRank

| 模型名称                 | url                                         |
|----------------------|---------------------------------------------|
| bce-reranker-base_v1 | local:bce:maidalun1020/bce-reranker-base_v1 |

## OCR

| 模型名称       | 参数                                 |
|------------|------------------------------------|
| paddle-ocr |                                    |
| olm_ocr    | olm_base_url、olm_api_key、olm_model |
| azure_ocr  | azure_endpoint、azure_api_key       |