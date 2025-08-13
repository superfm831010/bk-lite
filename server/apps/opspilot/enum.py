from django.db import models
from django.utils.translation import gettext_lazy as _


class ChannelChoices(models.TextChoices):
    ENTERPRISE_WECHAT = ("enterprise_wechat", _("Enterprise WeChat"))
    ENTERPRISE_WECHAT_BOT = ("enterprise_wechat_bot", _("Enterprise WeChat Bot"))
    WECHAT_OFFICIAL_ACCOUNT = ("wechat_official_account", _("WeChat Official Account"))
    DING_TALK = ("ding_talk", _("Ding Talk"))
    WEB = ("web", _("Web"))
    GITLAB = ("gitlab", _("GitLab"))


class BotTypeChoice(models.IntegerChoices):
    PILOT = (1, _("Pilot"))
    LOBE = (2, _("LobeChat"))


class SkillTypeChoices(models.IntegerChoices):
    BASIC_TOOL = 1, _("Basic Tool")
    KNOWLEDGE_TOOL = 2, _("Knowledge Tool")
    PLAN_EXECUTE = 3, _("Plan Execute")
    LATS = 4, _("Lats")


class LLMModelChoices(models.TextChoices):
    CHAT_GPT = "chat-gpt", "OpenAI"
    ZHIPU = "zhipu", "智谱AI"
    HUGGING_FACE = "hugging_face", "Hugging Face"
    DEEP_SEEK = "deep-seek", "DeepSeek"
    BAICHUAN = "Baichuan", "百川"
