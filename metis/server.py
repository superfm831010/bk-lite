import traceback

from langgraph.checkpoint.postgres import PostgresSaver
from sanic import Sanic
from sanic import json
from sanic.log import logger
from sanic.logging.default import LOGGING_CONFIG_DEFAULTS
import logging
from src.api import api
from src.core import graph
from src.core.env.core_settings import core_settings
from src.core.sanic_plus.auth.api_auth import auth
from src.core.sanic_plus.utils.config import YamlConfig
from src.core.sanic_plus.utils.crypto import PasswordCrypto
from src.embed.embed_builder import EmbedBuilder
from src.ocr.pp_ocr import PPOcr
from src.rerank.rerank_manager import ReRankManager

if core_settings.is_prod_mode():
    logger.info("生产模式下运行，加载鉴权配置....")
    crypto = PasswordCrypto(core_settings.secret_key)
    users = {
        "admin": crypto.encrypt(core_settings.admin_password),
    }


# 配置认证
@auth.verify_password
def verify_password(username, password) -> bool:
    if core_settings.is_debug_mode():
        return True

    if username in users:
        encrypted_password = users.get(username)
        return crypto.decrypt(encrypted_password) == crypto.decrypt(password)
    return False


def bootstrap() -> Sanic:
    config = YamlConfig(path="config.yml")

    logging.basicConfig(level=logging.INFO)
    LOGGING_CONFIG_DEFAULTS['formatters']['generic'] = {
        'class': 'src.core.sanic_plus.log.sanic_log_formater.SanicLogFormatter',
    }
    LOGGING_CONFIG_DEFAULTS['formatters']['access'] = {
        'class': 'src.core.sanic_plus.log.sanic_log_formater.SanicAccessFormatter',
    }
    app = Sanic("Metis", config=config, log_config=LOGGING_CONFIG_DEFAULTS)

    app.blueprint(api)

    @app.exception(Exception)
    async def global_api_exception(request, exception):
        error_traceback = traceback.format_exc()
        msg = f"全局异常捕获: {exception}, 请求路径: {request.path}, 请求参数: {request.args}\n堆栈信息: {error_traceback}"
        logger.error(msg)
        return json({}, status=500)

    # 配置启动钩子
    @app.before_server_start
    async def show_banner(app, loop):
        with open(f"src/asserts/banner.txt") as f:
            print(f.read())

        if core_settings.supabase_enabled():
            logger.info(f"启动supabase能力,supabase地址{core_settings.supabase_url}")

            from supabase import create_client
            app.ctx.supabase = create_client(
                core_settings.supabase_url, core_settings.supabase_key)

        if core_settings.graphiti_enabled():
            logger.info(f"启动Graphiti能力, Neo4j地址{core_settings.neo4j_host}")

            from src.rag.graph_rag.graphiti.graphiti_rag import GraphitiRAG
            rag = GraphitiRAG()
            await rag.setup_graph()

    @app.command
    def sync_db():
        try:
            with PostgresSaver.from_conn_string(core_settings.db_uri) as checkpointer:
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
        ReRankManager.get_rerank_instance(
            'local:bce:maidalun1020/bce-reranker-base_v1')

        logger.info("download PaddleOCR")
        PPOcr()

    return app
