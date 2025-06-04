from src.tools.http_request_tools_plus import http_get, http_post, http_put, http_delete
import os

import logging

logger = logging.getLogger(__name__)


# def test_http_get_requests():
#     result = http_get.run('{"movie_id":36154853}', config={
#         'configurable': {
#             "url": os.environ['TEST_HTTP_GET_URL'],
#             "headers": os.environ['TEST_HTTP_GET_HEADERS'],
#         }
#     })  # type: ignore
#
#     logger.info(result)


# def test_http_get_request_paramss():
#     result = http_get.run('{"limit":50}', config={
#         'configurable': {
#             "url": 'https://m.douban.com/rexxar/api/v2/subject/recent_hot/movie?limit={{limit}}',
#             "headers": '{"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36","referer":"https://movie.douban.com/","Origin":"https://movie.douban.com"}',
#         }
#     })  # type: ignore
#
#     logger.info(result)
