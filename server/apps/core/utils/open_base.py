import logging
from typing import Callable, Any, Optional
from functools import wraps

from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSet

# 配置日志记录器
logger = logging.getLogger(__name__)

# 常量定义
LOGIN_EXEMPT_ATTR = 'login_exempt'


def login_exempt(view_func: Callable) -> Callable:
    """
    标记视图函数免于登录保护的装饰器
    
    Args:
        view_func: 需要豁免登录的视图函数
        
    Returns:
        装饰后的视图函数
        
    Raises:
        TypeError: 当传入的不是可调用对象时
    """
    if not callable(view_func):
        logger.error(f"login_exempt装饰器接收到非可调用对象: {type(view_func)}")
        raise TypeError("login_exempt装饰器只能应用于可调用对象")
    
    @wraps(view_func)
    def wrapped_view(*args: Any, **kwargs: Any) -> Any:
        """包装后的视图函数"""
        try:
            logger.debug(f"执行豁免登录的视图函数: {view_func.__name__}")
            return view_func(*args, **kwargs)
        except Exception as e:
            logger.error(f"豁免登录视图函数 {view_func.__name__} 执行异常: {str(e)}")
            raise
    
    # 设置豁免登录标记
    setattr(wrapped_view, LOGIN_EXEMPT_ATTR, True)
    logger.info(f"视图函数 {view_func.__name__} 已设置为豁免登录")
    
    return wrapped_view


class OpenAPIViewSet(ViewSet):
    """
    开放API视图集基类
    
    提供无需身份验证的API接口基础功能，自动豁免CSRF和登录验证
    """
    permission_classes = [AllowAny]

    @classmethod
    def as_view(cls, actions: Optional[dict] = None, **kwargs: Any) -> Callable:
        """
        创建视图实例，自动应用登录豁免和CSRF豁免
        
        Args:
            actions: 视图集的动作映射字典
            **kwargs: 其他关键字参数
            
        Returns:
            配置了豁免策略的视图函数
            
        Raises:
            Exception: 视图创建过程中的异常
        """
        try:
            logger.info(f"创建OpenAPIViewSet实例: {cls.__name__}")
            
            # 调用父类方法创建视图
            view = super(ViewSet, cls).as_view(actions=actions, **kwargs)
            
            # 应用装饰器：先登录豁免，再CSRF豁免
            decorated_view = csrf_exempt(login_exempt(view))
            
            logger.info(f"OpenAPIViewSet {cls.__name__} 创建成功，已应用登录和CSRF豁免")
            return decorated_view
            
        except Exception as e:
            logger.error(f"创建OpenAPIViewSet {cls.__name__} 失败: {str(e)}")
            raise

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """
        子类初始化钩子，记录继承信息
        
        Args:
            **kwargs: 其他关键字参数
        """
        super().__init_subclass__(**kwargs)
        logger.debug(f"OpenAPIViewSet子类已注册: {cls.__name__}")
