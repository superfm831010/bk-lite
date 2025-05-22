import time

from apps.opspilot.bot_mgmt.models import Bot
from apps.opspilot.utils.docker_client import DockerClient
import logging

logger = logging.getLogger(__name__)


def test_pilot_lifecycle():
    client = DockerClient()
    rs = client.list_pilot()
    logger.info(rs)

    bot = Bot(
        id=1,
        api_token="1234",
        enable_ssl=False,
        bot_domain=""
    )
    client.start_pilot(bot)

    time.sleep(2)
    client.stop_pilot(1)
