from apps.core.logger import opspilot_logger as logger
from apps.opspilot.config import LOBE_RUNTIME
from apps.opspilot.models import Bot
from apps.opspilot.utils.lobe_chat_app.docker_client import LobeDockerClient
from apps.opspilot.utils.lobe_chat_app.kubernetes_client import LobeKubernetesClient


class LobeChatClient(object):
    def __init__(self):
        """
        初始化Pilot客户端
        根据环境变量PILOT_RUNTIME决定使用Kubernetes还是Docker
        """
        if LOBE_RUNTIME.lower() == "docker":
            logger.info("使用Docker运行时")
            self.client = LobeDockerClient()
        else:
            logger.info("使用Kubernetes运行时")
            self.client = LobeKubernetesClient()

    def start_pilot(self, bot: Bot):
        logger.info(f"启动Pilot: {bot.id}")
        try:
            result = self.client.start_pilot(bot)
        except Exception as e:
            logger.exception(f"启动Pilot失败: {e}")
            raise Exception("无法连接到Pilot服务，请检查服务是否正常运行。")
        return result

    def stop_pilot(self, bot_id):
        try:
            result = self.client.stop_pilot(bot_id)
        except Exception as e:
            logger.exception(f"停止Pilot失败: {e}")
            raise Exception("无法连接到Pilot服务，请检查服务是否正常运行。")
        return result

    def list_pilot(self):
        result = self.client.list_pilot()
        return result
