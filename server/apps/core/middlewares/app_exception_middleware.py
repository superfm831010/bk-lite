import json
import logging
import traceback
from typing import Optional, Any, Dict

from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin

from apps.core.exceptions.base_app_exception import BaseAppException
from apps.core.utils.web_utils import WebUtils

logger = logging.getLogger("app")

# 常量定义
DEFAULT_ERROR_MESSAGE = "系统异常,请联系管理员处理"
DEFAULT_ERROR_STATUS_CODE = 500
MAX_LOG_PARAMS_LENGTH = 1000
SENSITIVE_FIELDS = {'password', 'token', 'secret', 'key', 'authorization'}


class AppExceptionMiddleware(MiddlewareMixin):
    
    def process_exception(self, request: HttpRequest, exception: Exception) -> Optional[HttpResponse]:
        """
        app后台错误统一处理
        
        Args:
            request: Django请求对象
            exception: 捕获的异常对象
            
        Returns:
            HttpResponse: 错误响应或None
        """
        try:
            self.exception = exception
            self.request = request
            
            # 获取客户端信息用于日志记录
            client_info = self._get_client_info(request)
            
            # 处理用户主动抛出的异常
            if isinstance(exception, BaseAppException):
                return self._handle_app_exception(exception, client_info)
            
            # 处理未捕获的系统异常
            return self._handle_system_exception(exception, client_info)
            
        except Exception as middleware_error:
            # 中间件自身异常处理，防止异常处理逻辑出错
            logger.critical(
                f"异常处理中间件自身发生错误: {str(middleware_error)}, "
                f"原始异常: {str(exception)}, "
                f"请求路径: {getattr(request, 'path', 'unknown')}"
            )
            return WebUtils.response_error(
                error_message=DEFAULT_ERROR_MESSAGE, 
                status_code=DEFAULT_ERROR_STATUS_CODE
            )
    
    def _handle_app_exception(self, exception: BaseAppException, client_info: Dict[str, Any]) -> HttpResponse:
        """
        处理业务异常
        
        Args:
            exception: 业务异常对象
            client_info: 客户端信息
            
        Returns:
            HttpResponse: 错误响应
        """
        logger.log(
            exception.LOG_LEVEL,
            f"业务异常 - 错误码: {exception.ERROR_CODE}, "
            f"错误信息: {exception.message}, "
            f"客户端IP: {client_info.get('client_ip', 'unknown')}, "
            f"用户: {client_info.get('username', 'anonymous')}, "
            f"请求路径: {client_info.get('path', 'unknown')}, "
            f"请求方法: {client_info.get('method', 'unknown')}, "
            f"异常参数: {exception.args}, "
            f"堆栈信息: {traceback.format_exc()}"
        )
        
        return WebUtils.response_error(
            error_message=exception.message, 
            status_code=exception.STATUS_CODE
        )
    
    def _handle_system_exception(self, exception: Exception, client_info: Dict[str, Any]) -> HttpResponse:
        """
        处理系统异常
        
        Args:
            exception: 系统异常对象
            client_info: 客户端信息
            
        Returns:
            HttpResponse: 错误响应
        """
        # 获取安全的请求参数
        safe_params = self._get_safe_request_params()
        
        logger.error(
            f"系统异常 - 异常类型: {type(exception).__name__}, "
            f"异常信息: {str(exception)}, "
            f"客户端IP: {client_info.get('client_ip', 'unknown')}, "
            f"用户: {client_info.get('username', 'anonymous')}, "
            f"请求路径: {client_info.get('path', 'unknown')}, "
            f"请求方法: {client_info.get('method', 'unknown')}, "
            f"请求参数: {safe_params}, "
            f"User-Agent: {client_info.get('user_agent', 'unknown')}, "
            f"堆栈信息: {traceback.format_exc()}"
        )
        
        return WebUtils.response_error(
            error_message=DEFAULT_ERROR_MESSAGE, 
            status_code=DEFAULT_ERROR_STATUS_CODE
        )
    
    def _get_client_info(self, request: HttpRequest) -> Dict[str, Any]:
        """
        获取客户端信息
        
        Args:
            request: Django请求对象
            
        Returns:
            Dict: 客户端信息字典
        """
        client_info = {
            'client_ip': self._get_client_ip(request),
            'username': self._get_username(request),
            'path': getattr(request, 'path', 'unknown'),
            'method': getattr(request, 'method', 'unknown'),
            'user_agent': request.META.get('HTTP_USER_AGENT', 'unknown')
        }
        return client_info
    
    def _get_client_ip(self, request: HttpRequest) -> str:
        """
        获取客户端真实IP地址
        
        Args:
            request: Django请求对象
            
        Returns:
            str: 客户端IP地址
        """
        # 优先从X-Forwarded-For获取真实IP
        forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if forwarded_for:
            # 取第一个IP（最原始的客户端IP）
            return forwarded_for.split(',')[0].strip()
        
        # 备用方案：从REMOTE_ADDR获取
        return request.META.get('REMOTE_ADDR', 'unknown')
    
    def _get_username(self, request: HttpRequest) -> str:
        """
        安全获取用户名
        
        Args:
            request: Django请求对象
            
        Returns:
            str: 用户名或匿名标识
        """
        try:
            if hasattr(request, 'user') and hasattr(request.user, 'username'):
                return request.user.username
        except Exception:
            # 防止用户对象访问异常
            pass
        return 'anonymous'
    
    def _get_safe_request_params(self) -> str:
        """
        获取安全的请求参数（过滤敏感信息）
        
        Returns:
            str: 安全的参数字符串
        """
        try:
            method = getattr(self.request, 'method', None)
            if not method:
                return "无法获取请求方法"
            
            # 获取请求参数
            params_data = getattr(self.request, method, None)
            if params_data is None:
                return f"请求方法 {method} 无参数数据"
            
            # 转换为字典并过滤敏感字段
            if hasattr(params_data, 'dict'):
                params_dict = params_data.dict()
            else:
                params_dict = dict(params_data) if params_data else {}
            
            # 过滤敏感字段
            safe_params = {}
            for key, value in params_dict.items():
                if any(sensitive in key.lower() for sensitive in SENSITIVE_FIELDS):
                    safe_params[key] = '***FILTERED***'
                else:
                    safe_params[key] = value
            
            # 转换为JSON字符串并限制长度
            params_str = json.dumps(safe_params, ensure_ascii=False, default=str)
            if len(params_str) > MAX_LOG_PARAMS_LENGTH:
                params_str = params_str[:MAX_LOG_PARAMS_LENGTH] + "...(truncated)"
            
            return params_str
            
        except Exception as e:
            return f"参数解析异常: {str(e)}"
