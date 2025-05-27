import logging

from django.conf import settings
from django.contrib import auth
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import gettext as _

from apps.core.utils.web_utils import WebUtils


class AuthMiddleware(MiddlewareMixin):
    # 豁免路径常量
    EXEMPT_PATHS = [
        "/swagger/",
        "/admin/",
        "/accounts/",
    ]
    
    def __init__(self, get_response):
        super().__init__(get_response)
        self.logger = logging.getLogger(__name__)

    def process_view(self, request, view, args, kwargs):
        """
        处理视图请求的认证逻辑
        """
        try:
            # 检查API豁免和路径豁免
            if self._is_exempt_request(request, view):
                self.logger.debug(f"Request to {request.path} is exempt from auth")
                return None

            # 检查登录豁免
            if self._is_login_exempt(view):
                self.logger.debug(f"View {view.__name__} is login exempt")
                return None

            # 执行Token认证
            return self._authenticate_token(request)
            
        except Exception as e:
            self.logger.error(f"Authentication error for {request.path}: {str(e)}")
            return WebUtils.response_401(_("Authentication failed"))

    def _is_exempt_request(self, request, view):
        """
        检查请求是否豁免认证
        """
        # 检查视图和请求的豁免标记
        if getattr(view, "api_exempt", False) or getattr(request, "api_pass", False):
            return True
        
        # 检查路径豁免
        request_path = request.path
        for exempt_path in self.EXEMPT_PATHS:
            if request_path == exempt_path.rstrip('/') or request_path.startswith(exempt_path):
                return True
        
        return False

    def _is_login_exempt(self, view):
        """
        检查视图是否豁免登录
        """
        return getattr(view, "login_exempt", False)

    def _authenticate_token(self, request):
        """
        执行Token认证
        """
        # 获取Token
        token_header = request.META.get(settings.AUTH_TOKEN_HEADER_NAME)
        if not token_header:
            self.logger.warning(f"Missing auth token for {request.path} from IP {self._get_client_ip(request)}")
            return WebUtils.response_401(_("please provide Token"))

        # 提取Bearer Token
        token = self._extract_bearer_token(token_header)
        if not token:
            self.logger.warning(f"Invalid token format for {request.path} from IP {self._get_client_ip(request)}")
            return WebUtils.response_401(_("please provide Token"))

        # 认证用户
        try:
            user = auth.authenticate(request=request, token=token)
            if user:
                auth.login(request, user)
                # 确保session有效
                if not request.session.session_key:
                    request.session.cycle_key()
                
                self.logger.info(f"User {user.username if hasattr(user, 'username') else 'unknown'} authenticated successfully for {request.path}")
                return None
            else:
                self.logger.warning(f"Invalid token for {request.path} from IP {self._get_client_ip(request)}")
                return WebUtils.response_401(_("please provide Token"))
                
        except Exception as e:
            self.logger.error(f"Token authentication failed for {request.path}: {str(e)}")
            return WebUtils.response_401(_("please provide Token"))

    def _extract_bearer_token(self, token_header):
        """
        从Authorization头中提取Bearer Token
        """
        if not token_header:
            return None
        
        # 处理Bearer格式
        if token_header.startswith("Bearer "):
            return token_header.split("Bearer ", 1)[-1].strip()
        
        # 如果没有Bearer前缀，直接返回token
        return token_header.strip()

    def _get_client_ip(self, request):
        """
        获取客户端IP地址
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', 'unknown')
