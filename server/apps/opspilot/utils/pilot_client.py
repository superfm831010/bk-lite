from apps.core.logger import opspilot_logger as logger
from apps.opspilot.config import PILOT_RUNTIME
from apps.opspilot.enum import BotTypeChoice
from apps.opspilot.models import Bot
from apps.opspilot.utils.rasa_app.docker_client import DockerClient
from apps.opspilot.utils.rasa_app.kubernetes_client import KubernetesClient


class PilotClient(object):
    def __init__(self):
        """
        初始化Pilot客户端
        根据环境变量PILOT_RUNTIME决定使用Kubernetes还是Docker
        """
        if PILOT_RUNTIME.lower() == "docker":
            logger.info("使用Docker运行时")
            self.client = DockerClient()
        else:
            logger.info("使用Kubernetes运行时")
            self.client = KubernetesClient()

    def start_pilot(self, bot: Bot):
        logger.info(f"启动Pilot: {bot.id}")
        try:
            if bot.bot_type == BotTypeChoice.PILOT:
                result = self.client.start_pilot(bot)
            else:
                result = self.client.start_lobe_chat(bot)
        except Exception as e:
            logger.exception(f"启动Pilot失败: {e}")
            raise Exception("无法连接到Pilot服务，请检查服务是否正常运行。")
        return result

    def stop_pilot(self, bot):
        try:
            if bot.bot_type == BotTypeChoice.PILOT:
                result = self.client.stop_pilot(bot.id)
            else:
                result = self.client.stop_lobe_chat(bot.id)
        except Exception as e:
            logger.exception(f"停止Pilot失败: {e}")
            raise Exception("无法连接到Pilot服务，请检查服务是否正常运行。")
        return result

    def list_pilot(self):
        result = self.client.list_pilot()
        return result
