
from sanic import Blueprint, json
from sanic_ext import validate

from src.core.sanic_plus.auth.api_auth import auth
from src.enhance.qa_enhance import QAEnhance
from src.entity.rag.enhance.qa_enhance_request import QAEnhanceRequest
from src.entity.rag.enhance.summarize_enhance_request import SummarizeEnhanceRequest
from src.summarize.summarize_manager import SummarizeManager

rag_enhance_api_router = Blueprint("rag_enhance_api_router", url_prefix="/rag")


@rag_enhance_api_router.post("/summarize_enhance")
@auth.login_required
@validate(json=SummarizeEnhanceRequest)
async def summarize_enhance(request, body: SummarizeEnhanceRequest):
    """
    文本摘要增强
    :param request:
    :param body:
    :return:
    """
    """
    文本摘要增强
    :param request:
    :param body:
    :return:
    """
    result = SummarizeManager.summarize(
        body.content, body.model, body.openai_api_base, body.openai_api_key)
    return json({"status": "success", "message": result})


@rag_enhance_api_router.post("/qa_pair_generate")
@auth.login_required
@validate(json=QAEnhanceRequest)
async def qa_pair_generate(request, body: QAEnhanceRequest):
    """
    QA 问答对生成
    :param request:
    :return:
    """
    """
    生成问答对
    :param request:
    :return:
    """
    qa_enhance = QAEnhance(body)
    result = qa_enhance.generate_qa()
    return json({"status": "success", "message": result})
