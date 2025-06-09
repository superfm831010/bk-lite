import copy

import nats_client
from apps.core.logger import logger
from apps.opspilot.model_provider_mgmt.models import EmbedModelChoices, LLMModelChoices, RerankModelChoices
from apps.opspilot.models import (
    Bot,
    EmbedProvider,
    KnowledgeBase,
    LLMModel,
    LLMSkill,
    OCRProvider,
    QuotaRule,
    RerankProvider,
    SkillTools,
)


@nats_client.register
def init_user_set(group_id, group_name):
    try:
        llm_model_list = LLMModel.objects.filter(is_demo=True)
        add_model_list = []
        name_list = set()
        for old_llm_model in llm_model_list:
            llm_model = copy.deepcopy(old_llm_model)
            llm_model.id = None
            llm_model.team = [group_id]
            llm_model.consumer_team = group_id
            llm_model.is_build_in = False
            llm_model.is_demo = False
            decrypted_llm_config = llm_model.decrypted_llm_config
            llm_model.llm_config = decrypted_llm_config
            add_model_list.append(llm_model)
            name_list.add(llm_model.name)
        LLMModel.objects.bulk_create(add_model_list)
        QuotaRule.objects.create(
            name=f"group-{group_name}-llm-quota",
            target_type="group",
            target_list=[group_id],
            rule_type="shared",
            file_size=50,
            unit="MB",
            skill_count=2,
            bot_count=2,
            token_set={key: {"value": 10, "unit": "thousand"} for key in name_list},
        )
        embed_model = EmbedProvider.objects.filter(name="FastEmbed(BAAI/bge-small-zh-v1.5)").first()
        if embed_model:
            embed_model.team.append(group_id)
            embed_model.save()
        return {"result": True}
    except Exception as e:
        logger.exception(e)
        return {"result": False, "message": str(e)}


@nats_client.register
def get_module_data(module, child_module, page, page_size, group_id):
    model_map = {
        "bot": Bot,
        "skill": LLMSkill,
        "knowledge": KnowledgeBase,
        "tools": SkillTools,
    }
    provider_model_map = {
        "llm_model": LLMModel,
        "ocr_model": OCRProvider,
        "embed_model": EmbedProvider,
        "rerank_model": RerankProvider,
    }
    if module != "provider":
        model = model_map[module]
    else:
        model = provider_model_map[child_module]
    queryset = model.objects.filter(team__contains=int(group_id))
    # 计算总数
    total_count = queryset.count()
    # 计算分页
    start = (page - 1) * page_size
    end = page * page_size
    # 获取当前页的数据
    data_list = queryset.values("id", "name")[start:end]

    return {
        "count": total_count,
        "items": list(data_list),
    }


@nats_client.register
def create_guest_provider(group_id):
    default_llm_model, _ = LLMModel.objects.get_or_create(
        name="GPT-4o",
        llm_model_type=LLMModelChoices.CHAT_GPT,
        is_build_in=False,
        team=[group_id],
        defaults={
            "llm_config": {
                "openai_api_key": "your_openai_api_key",
                "openai_base_url": "https://api.openai.com",
                "temperature": 0.7,
                "model": "gpt-4o",
                "is_demo": False,
            },
        },
    )
    rerank_model, _ = RerankProvider.objects.get_or_create(
        name="bce-reranker-base_v1",
        rerank_model_type=RerankModelChoices.LANG_SERVE,
        is_build_in=False,
        defaults={
            "rerank_config": {
                "base_url": "local:bce:maidalun1020/bce-reranker-base_v1",
                "api_key": "",
                "model": "bce-reranker-base_v1",
            },
            "team": [group_id],
        },
    )

    embed_model_1, _ = EmbedProvider.objects.get_or_create(
        name="bce-embedding-base_v1",
        embed_model_type=EmbedModelChoices.LANG_SERVE,
        is_build_in=False,
        team=[group_id],
        defaults={
            "embed_config": {
                "base_url": "local:huggingface_embedding:maidalun1020/bce-embedding-base_v1",
                "api_key": "",
                "model": "bce-embedding-base_v1",
            },
        },
    )
    embed_model_2, _ = EmbedProvider.objects.get_or_create(
        name="FastEmbed(BAAI/bge-small-zh-v1.5)",
        embed_model_type=EmbedModelChoices.LANG_SERVE,
        is_build_in=False,
        team=[group_id],
        defaults={
            "embed_config": {
                "base_url": "local:huggingface_embedding:BAAI/bge-small-zh-v1.5",
                "api_key": "",
                "model": "FastEmbed(BAAI/bge-small-zh-v1.5)",
            },
        },
    )
    paddle_ocr, _ = OCRProvider.objects.get_or_create(
        name="PaddleOCR",
        is_build_in=False,
        team=[group_id],
        defaults={
            "enabled": True,
        },
    )

    azure_ocr, _ = OCRProvider.objects.get_or_create(
        name="AzureOCR",
        is_build_in=False,
        team=[group_id],
        defaults={
            "enabled": True,
            "ocr_config": {
                "base_url": "http://ocr-server/azure_ocr",
                "api_key": "",
                "endpoint": "",
            },
        },
    )
    olm_ocr, _ = OCRProvider.objects.get_or_create(
        name="OlmOCR",
        is_build_in=False,
        team=[group_id],
        defaults={
            "enabled": True,
            "ocr_config": {"base_url": "http://ocr-server/olm_ocr", "api_key": ""},
        },
    )

    return {
        "result": True,
        "data": {
            "llm_model": {"id": default_llm_model.id, "name": default_llm_model.name},
            "rerank_model": {"id": rerank_model.id, "name": rerank_model.name},
            "embed_model": [{"id": model.id, "name": model.name} for model in [embed_model_1, embed_model_2]],
            "ocr_model": [{"id": model.id, "name": model.name} for model in [paddle_ocr, azure_ocr, olm_ocr]],
        },
    }
