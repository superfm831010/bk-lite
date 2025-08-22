from src.web.entity.rag.enhance.summarize_enhance_request import SummarizeEnhanceRequest
from src.core.summarize.textrank.textrank_sentence import TextRankSentence
from sanic.log import logger


class SummarizeManager:
    @classmethod
    def summarize(cls, req: SummarizeEnhanceRequest) -> str:
        if req.model.startswith('local:'):
            local_model = req.model.split(':')[1]
            if local_model == 'textrank':
                text_rank_model = TextRankSentence()
                text_rank_model.analyze(text=req.content, lower=True, source='all_filters')
                items = text_rank_model.get_key_sentences(num=1)
                return items[0].sentence

        logger.warn(f"没有找到对应的摘要模型: {req.model}, 使用默认的内容返回")
        return req.content
