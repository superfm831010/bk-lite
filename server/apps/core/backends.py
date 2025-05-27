import logging
import os
import traceback
from typing import Optional, Dict, Any

from django.contrib.auth.backends import ModelBackend
from django.core.cache import caches
from django.db import IntegrityError
from django.utils import translation

from apps.base.models import User, UserAPISecret
from apps.rpc.system_mgmt import SystemMgmt

logger = logging.getLogger("app")
cache = caches["db"]

# 常量定义
DEFAULT_LOCALE = "en"
CHINESE_LOCALE_MAPPING = {
    "zh-CN": "zh-Hans"
}
COOKIE_CURRENT_TEAM = "current_team"
CLIENT_ID_ENV_KEY = "CLIENT_ID"


class APISecretAuthBackend(ModelBackend):
    """API密钥认证后端"""
    
    def authenticate(self, request=None, username=None, password=None, api_token=None) -> Optional[User]:
        """
        使用API token进行用户认证
        
        Args:
            api_token: API认证令牌
            
        Returns:
            认证成功的用户对象或None
        """
        if not api_token:
            logger.debug("API token authentication failed: no token provided")
            return None
            
        logger.info(f"Attempting API token authentication for token: {api_token[:8]}...")
        
        try:
            user_secret = UserAPISecret.objects.filter(api_secret=api_token).first()
            if not user_secret:
                logger.warning(f"API token authentication failed: invalid token {api_token[:8]}...")
                return None
                
            user = User.objects.get(username=user_secret.username)
            user.group_list = [user_secret.team]
            
            logger.info(f"API token authentication successful for user: {user.username}")
            return user
            
        except User.DoesNotExist:
            logger.error(f"API token authentication failed: user {user_secret.username} not found")
            return None
        except Exception as e:
            logger.error(f"API token authentication error: {str(e)}")
            logger.debug(f"API token authentication exception details: {traceback.format_exc()}")
            return None


class AuthBackend(ModelBackend):
    """标准认证后端"""
    
    def authenticate(self, request=None, username=None, password=None, token=None) -> Optional[User]:
        """
        使用token进行用户认证
        
        Args:
            token: 认证令牌
            request: HTTP请求对象
            
        Returns:
            认证成功的用户对象或None
        """
        if not token:
            logger.debug("Token authentication failed: no token provided")
            return None
            
        logger.info(f"Attempting token authentication for token: {token[:8]}...")
        
        try:
            # 创建SystemMgmt客户端并验证token
            result = self._verify_token_with_system_mgmt(token)
            if not result:
                return None
                
            user_info = result.get("data")
            if not user_info:
                logger.error("Token verification returned empty user info")
                return None
                
            # 处理用户locale设置
            self._handle_user_locale(user_info)
            
            # 获取用户规则权限
            rules = self._get_user_rules(request, user_info)
            
            # 设置用户信息
            user = self.set_user_info(user_info, rules)
            if user:
                logger.info(f"Token authentication successful for user: {user.username}")
            
            return user
            
        except Exception as e:
            logger.error(f"Token authentication error: {str(e)}")
            logger.debug(f"Token authentication exception details: {traceback.format_exc()}")
            return None
    
    def _verify_token_with_system_mgmt(self, token: str) -> Optional[Dict[str, Any]]:
        """
        使用SystemMgmt验证token
        
        Args:
            token: 认证令牌
            
        Returns:
            验证结果字典或None
        """
        try:
            client = SystemMgmt()
            app = os.getenv(CLIENT_ID_ENV_KEY, "")
            
            if not app:
                logger.warning(f"Environment variable {CLIENT_ID_ENV_KEY} not set")
            
            result = client.verify_token(token, app)
            
            if not result.get("result"):
                logger.warning(f"Token verification failed for token: {token[:8]}...")
                return None
                
            logger.debug("Token verification successful")
            return result
            
        except Exception as e:
            logger.error(f"SystemMgmt token verification error: {str(e)}")
            raise
    
    def _handle_user_locale(self, user_info: Dict[str, Any]) -> None:
        """
        处理用户locale设置
        
        Args:
            user_info: 用户信息字典
        """
        locale = user_info.get("locale")
        if not locale:
            return
            
        # 处理中文locale映射
        if locale in CHINESE_LOCALE_MAPPING:
            user_info["locale"] = CHINESE_LOCALE_MAPPING[locale]
            locale = user_info["locale"]
            
        try:
            translation.activate(locale)
            logger.debug(f"User locale set to: {locale}")
        except Exception as e:
            logger.warning(f"Failed to activate locale {locale}: {str(e)}")
    
    def _get_user_rules(self, request, user_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取用户规则权限
        
        Args:
            request: HTTP请求对象
            user_info: 用户信息字典
            
        Returns:
            用户规则字典
        """
        if not request or not hasattr(request, 'COOKIES'):
            logger.debug("No request or cookies available for rule retrieval")
            return {}
            
        current_group = request.COOKIES.get(COOKIE_CURRENT_TEAM)
        if not current_group:
            logger.debug("No current team found in cookies")
            return {}
            
        username = user_info.get("username")
        if not username:
            logger.warning("No username found in user_info for rule retrieval")
            return {}
            
        try:
            client = SystemMgmt()
            app = os.getenv(CLIENT_ID_ENV_KEY, "")
            rules = client.get_user_rules(app, current_group, username)
            logger.debug(f"Retrieved rules for user {username} in group {current_group}")
            return rules or {}
        except Exception as e:
            logger.error(f"Failed to get user rules for {username}: {str(e)}")
            return {}

    @staticmethod
    def set_user_info(user_info: Dict[str, Any], rules: Dict[str, Any]) -> Optional[User]:
        """
        设置用户信息
        
        Args:
            user_info: 用户信息字典
            rules: 用户规则字典
            
        Returns:
            用户对象或None
        """
        username = user_info.get("username")
        if not username:
            logger.error("Cannot create user: username not provided in user_info")
            return None
            
        try:
            user, created = User.objects.get_or_create(username=username)
            
            # 更新用户基本信息
            user.email = user_info.get("email", "")
            user.is_superuser = bool(user_info.get("is_superuser", False))
            user.is_staff = user.is_superuser
            user.group_list = user_info.get("group_list", [])
            user.roles = user_info.get("roles", [])
            user.locale = user_info.get("locale", DEFAULT_LOCALE)
            
            user.save()
            
            # 设置运行时属性
            user.rules = rules
            user.permission = set(user_info.get("permission") or [])
            
            action = "created" if created else "updated"
            logger.info(f"User {username} {action} successfully")
            
            return user
            
        except IntegrityError as e:
            logger.error(f"Database integrity error for user {username}: {str(e)}")
            logger.debug(f"IntegrityError details: {traceback.format_exc()}")
            return None
        except Exception as e:
            logger.error(f"Failed to create/update user {username}: {str(e)}")
            logger.debug(f"User creation exception details: {traceback.format_exc()}")
            return None
