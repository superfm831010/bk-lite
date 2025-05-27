import logging
from django.conf import settings
from django.contrib import auth
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import gettext as _
from rest_framework import status

from apps.core.utils.web_utils import WebUtils

logger = logging.getLogger(__name__)


class APISecretMiddleware(MiddlewareMixin):
    """API令牌认证中间件"""

    # 常量定义，避免魔法变量
    API_PASS_ATTR = "api_pass"
    TOKEN_MISSING_MSG = "token validation failed"

    def process_request(self, request):
        """
        处理请求的API令牌验证
        
        :param request: Django请求对象
        :return: None表示继续处理请求，HttpResponse表示直接返回响应
        """
        # 获取客户端IP，用于日志记录（不记录敏感信息）
        client_ip = self._get_client_ip(request)
        request_path = getattr(request, 'path', 'unknown')

        logger.info(
            "API令牌验证开始 - IP: %s, 路径: %s, 方法: %s",
            client_ip,
            request_path,
            getattr(request, 'method', 'unknown')
        )

        # 获取API令牌
        token = self._get_api_token(request)
        if token is None:
            setattr(request, self.API_PASS_ATTR, False)
            return None

        # 验证令牌并进行用户认证
        try:
            user = auth.authenticate(request=request, api_token=token)
            if user is not None:
                return self._handle_successful_auth(request, user, client_ip, request_path)
            else:
                return self._handle_failed_auth(request, client_ip, request_path)

        except Exception as e:
            logger.error(
                "API令牌验证异常 - IP: %s, 路径: %s, 错误: %s",
                client_ip,
                request_path,
                str(e),
                exc_info=True
            )
            return WebUtils.response_error(
                error_message=_(self.TOKEN_MISSING_MSG),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _get_client_ip(self, request):
        """
        获取客户端IP地址
        
        :param request: Django请求对象
        :return: 客户端IP地址字符串
        """
        # 优先获取代理转发的真实IP
        x_forwarded_for = getattr(request.META, 'get', lambda x: None)('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = getattr(request.META, 'get', lambda x: 'unknown')('REMOTE_ADDR')
        return ip or 'unknown'

    def _get_api_token(self, request):
        """
        从请求头中获取API令牌
        
        :param request: Django请求对象
        :return: API令牌字符串或None
        """
        header_name = getattr(settings, 'API_TOKEN_HEADER_NAME', None)
        if not header_name:
            logger.error("API_TOKEN_HEADER_NAME配置缺失")
            return None

        token = getattr(request.META, 'get', lambda x: None)(header_name)
        if token:
            # 记录令牌长度用于调试，但不记录实际值
            logger.debug("API令牌已获取 - 长度: %d", len(token))
        return token

    def _handle_successful_auth(self, request, user, client_ip, request_path):
        """
        处理认证成功的情况
        
        :param request: Django请求对象
        :param user: 认证成功的用户对象
        :param client_ip: 客户端IP
        :param request_path: 请求路径
        :return: None
        """
        logger.info(
            "API令牌验证成功 - IP: %s, 路径: %s, 用户: %s",
            client_ip,
            request_path,
            getattr(user, 'username', 'unknown') if user else 'unknown'
        )

        setattr(request, self.API_PASS_ATTR, True)
        auth.login(request, user)

        # 确保会话密钥存在
        session_key = getattr(request.session, 'session_key', None)
        if not session_key:
            if hasattr(request.session, 'cycle_key'):
                request.session.cycle_key()
                logger.debug("为用户创建新的会话密钥")
            else:
                logger.warning("无法创建会话密钥：session.cycle_key方法不存在")

        return None

    def _handle_failed_auth(self, request, client_ip, request_path):
        """
        处理认证失败的情况
        
        :param request: Django请求对象
        :param client_ip: 客户端IP
        :param request_path: 请求路径
        :return: 错误响应
        """
        logger.warning(
            "API令牌验证失败 - IP: %s, 路径: %s",
            client_ip,
            request_path
        )

        return WebUtils.response_error(
            error_message=_(self.TOKEN_MISSING_MSG),
            status_code=status.HTTP_403_FORBIDDEN
        )
