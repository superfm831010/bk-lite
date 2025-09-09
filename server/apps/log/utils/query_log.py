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
                timeout=None,  # 允许长连接
            )
            response.raise_for_status()

            # 确保响应使用UTF-8编码
            response.encoding = 'utf-8'

            # 使用生成器返回数据，手动处理编码确保正确显示
            for line in response.iter_lines(chunk_size=1):
                if line:
                    # 手动解码确保UTF-8编码正确
                    try:
                        decoded_line = line.decode('utf-8')
                        yield decoded_line
                    except UnicodeDecodeError:
                        # 如果UTF-8解码失败，尝试其他编码
                        try:
                            decoded_line = line.decode('gbk')
                            yield decoded_line
                        except UnicodeDecodeError:
                            # 最后使用errors='replace'避免异常
                            decoded_line = line.decode('utf-8', errors='replace')
                            yield decoded_line

        except requests.exceptions.RequestException as e:
            logger.error("VictoriaLogs tail连接失败", extra={'error': str(e)})
            raise
        except Exception as e:
            logger.error(f"Tail接口意外错误", extra={
                'query_summary': query[:50] + '...' if len(query) > 50 else query,
                'error': str(e)
            })
            raise

    async def tail_async(self, query):
        """异步版本的tail方法，解决Django StreamingHttpResponse警告"""
        data = {"query": query}

        try:
            # 在执行器中运行同步请求以避免阻塞事件循环
            loop = asyncio.get_event_loop()

            def _make_request():
                response = requests.post(
                    f"{self.host}/select/logsql/tail",
                    params=data,
                    auth=(self.username, self.password),
                    verify=self.ssl_verify,
                    stream=True,
                    timeout=None,
                )
                # 确保响应使用UTF-8编码
                response.encoding = 'utf-8'
                return response

            response = await loop.run_in_executor(None, _make_request)
            response.raise_for_status()

            # 异步生成器，手动处理编码
            for line in response.iter_lines(chunk_size=1):
                if line:
                    # 手动解码确保UTF-8编码正确
                    try:
                        decoded_line = line.decode('utf-8')
                        await asyncio.sleep(0)  # 让出控制权
                        yield decoded_line
                    except UnicodeDecodeError:
                        # 如果UTF-8解码失败，尝试其他编码
                        try:
                            decoded_line = line.decode('gbk')
                            await asyncio.sleep(0)
                            yield decoded_line
                        except UnicodeDecodeError:
                            # 最后使用errors='replace'避免异常
                            decoded_line = line.decode('utf-8', errors='replace')
                            await asyncio.sleep(0)
                            yield decoded_line

        except requests.exceptions.RequestException as e:
            logger.error("异步VictoriaLogs tail连接失败", extra={'error': str(e)})
            raise
        except Exception as e:
            logger.error(f"异步Tail接口意外错误", extra={
                'query_summary': query[:50] + '...' if len(query) > 50 else query,
                'error': str(e)
            })
            raise
