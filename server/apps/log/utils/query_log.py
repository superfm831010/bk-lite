import json
import asyncio
import requests
from apps.log.constants import VICTORIALOGS_HOST, VICTORIALOGS_USER, VICTORIALOGS_PWD, VICTORIALOGS_SSL_VERIFY
from apps.core.logger import log_logger as logger


class VictoriaMetricsAPI:
    def __init__(self):
        self.host = VICTORIALOGS_HOST
        self.username = VICTORIALOGS_USER
        self.password = VICTORIALOGS_PWD
        self.ssl_verify = VICTORIALOGS_SSL_VERIFY

    def query(self, query, start, end, limit=10):
        data = {"query": query, "start": start, "end": end, "limit": limit}
        response = requests.post(
            f"{self.host}/select/logsql/query",
            params=data,
            auth=(self.username, self.password),
            verify=self.ssl_verify,
        )
        response.raise_for_status()
        result = []
        for line in response.text.strip().splitlines():
            if line:
                result.append(json.loads(line))
        return result

    def hits(self, query, start, end, field, fields_limit=5, step="5m"):
        data = {"query": query, "start": start, "end": end, "field": field, "fields_limit": fields_limit, "step": step}

        response = requests.post(
            f"{self.host}/select/logsql/hits",
            params=data,
            auth=(self.username, self.password),
            verify=self.ssl_verify,
        )
        response.raise_for_status()
        return response.json()

    def tail(self, query):
        """tail是一个长连接接口，用于实时获取日志数据"""
        data = {"query": query}

        try:
            response = requests.post(
                f"{self.host}/select/logsql/tail",
                params=data,
                auth=(self.username, self.password),
                verify=self.ssl_verify,
                stream=True,
                timeout=(10, 120),  # 关键修复：连接超时10秒，读取超时120秒
                headers={
                    'Accept': 'application/x-ndjson, text/plain, */*',
                    'Connection': 'keep-alive',
                    'Cache-Control': 'no-cache'
                }
            )
            response.raise_for_status()

            # 确保响应使用UTF-8编码
            response.encoding = 'utf-8'

            logger.info("VictoriaLogs tail连接成功", extra={
                'query_preview': query[:100] + '...' if len(query) > 100 else query,
                'host': self.host
            })

            # 使用生成器返回数据，优化性能和错误处理
            line_count = 0
            for line in response.iter_lines(chunk_size=8192, decode_unicode=True):
                if line:
                    line_count += 1
                    try:
                        yield line.strip()

                        # 每1000行记录一次状态，减少日志量
                        if line_count % 1000 == 0:
                            logger.debug("VictoriaLogs数据流状态", extra={
                                'lines_received': line_count
                            })

                    except Exception as line_error:
                        logger.warning("处理VictoriaLogs数据行失败", extra={
                            'error': str(line_error),
                            'line_preview': line[:100] if line else 'empty'
                        })
                        continue  # 跳过错误行，继续处理

        except requests.exceptions.ConnectTimeout:
            logger.error("VictoriaLogs连接超时", extra={
                'host': self.host,
                'timeout': '10秒'
            })
            raise
        except requests.exceptions.ReadTimeout:
            logger.error("VictoriaLogs读取超时", extra={
                'host': self.host,
                'timeout': '120秒'
            })
            raise
        except requests.exceptions.RequestException as e:
            logger.error("VictoriaLogs tail连接失败", extra={
                'error': str(e),
                'host': self.host,
                'query_preview': query[:50] + '...' if len(query) > 50 else query
            })
            raise
        except Exception as e:
            logger.error("VictoriaLogs tail意外错误", extra={
                'error': str(e),
                'error_type': type(e).__name__,
                'query_preview': query[:50] + '...' if len(query) > 50 else query
            })
            raise
