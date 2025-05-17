import os
from dotenv import load_dotenv
from sanic import Sanic
from sanic.logging.default import LOGGING_CONFIG_DEFAULTS
import src.api as blueprints
from src.core.sanic_plus.autodiscover import autodiscover
from src.core.web.api_auth import auth
from src.core.web.config import YamlConfig
from src.core.web.crypto import PasswordCrypto
from sanic.log import logger
from langgraph.checkpoint.postgres import PostgresSaver
from sanic import json
from src.embed.embed_builder import EmbedBuilder
from src.ocr.pp_ocr import PPOcr
from src.rerank.rerank_manager import ReRankManager

# 加载环境变量和配置
load_dotenv()

if os.getenv('MODE', 'DEBUG') != 'DEBUG':
    crypto = PasswordCrypto(os.getenv("SECRET_KEY"))
    users = {
        "admin": crypto.encrypt(os.getenv("ADMIN_PASSWORD")),
    }


# 配置认证
@auth.verify_password
def verify_password(username, password):
    if os.getenv('MODE', 'DEBUG') == 'DEBUG':
        return True

    if username in users:
        encrypted_password = users.get(username)
        return crypto.decrypt(encrypted_password) == crypto.decrypt(password)
    return False


def bootstrap():
    config = YamlConfig(path="config.yml")
    LOGGING_CONFIG_DEFAULTS['formatters']['generic'] = {
        'class': 'src.core.sanic_plus.sanic_log_formater.SanicLogFormatter',
    }
    LOGGING_CONFIG_DEFAULTS['formatters']['access'] = {
        'class': 'src.core.sanic_plus.sanic_log_formater.SanicAccessFormatter',
    }
    app = Sanic("Metis", config=config, log_config=LOGGING_CONFIG_DEFAULTS)

    autodiscover(
        app,
        blueprints,
        recursive=True,
    )

    @app.exception(Exception)
    async def global_api_exception(request, exception):
        msg = f"全局异常捕获: {exception}, 请求路径: {request.path}, 请求参数: {request.args}, 请求体: {request.json}"
        logger.error(msg)
        return json({}, status=500)

    # 配置启动钩子
    @app.before_server_start
    async def show_banner(app, loop):
        with open(f"src/asserts/banner.txt") as f:
            print(f.read())

        if os.getenv('SUPABASE_URL') and os.getenv('SUPABASE_KEY'):
            logger.info(f"启动supabase能力,supabase地址{os.getenv('SUPABASE_URL')}")
            from supabase import create_client, Client
            app.ctx.supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

    @app.command
    def sync_db():
        try:
            with PostgresSaver.from_conn_string(os.getenv('DB_URI')) as checkpointer:
                checkpointer.setup()
        except Exception as e:
            pass
        logger.info("setup langgraph checkpoint finished")

    @app.command
    async def download_models():
        logger.info("download HuggingFace Embed Models")
        EmbedBuilder().get_embed('local:huggingface_embedding:BAAI/bge-small-zh-v1.5')
        EmbedBuilder().get_embed('local:huggingface_embedding:maidalun1020/bce-embedding-base_v1')

        logger.info("download BCE ReRank Models")
        ReRankManager.get_rerank_instance('local:bce:maidalun1020/bce-reranker-base_v1')

        logger.info("download PaddleOCR")
        PPOcr()

    return app
