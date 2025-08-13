from sanic import Blueprint
from sanic_ext import validate

from src.core.sanic_plus.auth.api_auth import auth
from src.entity.rag.enhance.answer_generate_request import AnswerGenerateRequest
from src.services.rag.qa_enhance_service import QAEnhanceService
from src.entity.common.common_response import CommonResponse
from src.entity.rag.enhance.qa_enhance_request import QAEnhanceRequest
from src.entity.rag.enhance.question_generate_request import QuestionGenerateRequest
from src.entity.rag.enhance.summarize_enhance_request import SummarizeEnhanceRequest
from src.summarize.summarize_manager import SummarizeManager

rag_enhance_api_router = Blueprint("rag_enhance_api_router", url_prefix="/rag")


@rag_enhance_api_router.post("/summarize_enhance")
@auth.login_required
@validate(json=SummarizeEnhanceRequest)
async def summarize_enhance(request, body: SummarizeEnhanceRequest):
    result = SummarizeManager.summarize(body)
    return CommonResponse.success(result)


@rag_enhance_api_router.post("/qa_pair_generate")
@auth.login_required
@validate(json=QAEnhanceRequest)
async def qa_pair_generate(request, body: QAEnhanceRequest):
    result = QAEnhanceService.generate_qa(body)
    return CommonResponse.success(result)


@rag_enhance_api_router.post("/question_generation")
@auth.login_required
@validate(json=QuestionGenerateRequest)
async def question_generation(request, body: QuestionGenerateRequest):
    result = QAEnhanceService.generate_question(body)
    return CommonResponse.success(result)

@rag_enhance_api_router.post("/answer_generation")
@auth.login_required
@validate(json=AnswerGenerateRequest)
async def answer_generation(request, body: AnswerGenerateRequest):
    result = QAEnhanceService.generate_answer(body)
    return CommonResponse.success(result)
