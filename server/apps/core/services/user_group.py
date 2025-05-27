import logging
from typing import Dict, Any, Optional, List

from apps.core.utils.user_group import Group
from apps.rpc.system_mgmt import SystemMgmt

logger = logging.getLogger(__name__)

class UserGroup:
    # 常量定义，避免魔法变量
    DEFAULT_SEARCH_QUERY = ""
    DEFAULT_QUERY_PARAMS = {"search": DEFAULT_SEARCH_QUERY}

    @staticmethod
    def get_system_mgmt_client() -> SystemMgmt:
        """获取系统管理客户端"""
        try:
            system_mgmt_client = SystemMgmt()
            logger.info("Successfully created SystemMgmt client")
            return system_mgmt_client
        except Exception as e:
            logger.error(f"Failed to create SystemMgmt client: {e}")
            raise

    @classmethod
    def user_list(cls, system_mgmt_client: SystemMgmt, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """用户列表
        
        Args:
            system_mgmt_client: 系统管理客户端
            query_params: 查询参数
            
        Returns:
            包含用户数量和用户列表的字典
        """
        if not system_mgmt_client:
            logger.error("SystemMgmt client is None")
            raise ValueError("SystemMgmt client cannot be None")
            
        if not isinstance(query_params, dict):
            logger.error(f"Invalid query_params type: {type(query_params)}")
            raise TypeError("query_params must be a dictionary")

        try:
            logger.info(f"Searching users with params: {query_params}")
            result = system_mgmt_client.search_users(query_params)
            
            if not isinstance(result, dict) or "data" not in result:
                logger.error(f"Invalid result format from search_users: {result}")
                raise ValueError("Invalid response format from search_users")
                
            data = result["data"]
            if not isinstance(data, dict):
                logger.error(f"Invalid data format in result: {data}")
                raise ValueError("Invalid data format in search result")
                
            # 安全地获取数据，避免KeyError
            count = data.get("count", 0)
            users = data.get("users", [])
            
            logger.info(f"Successfully retrieved {count} users")
            return {"count": count, "users": users}
            
        except Exception as e:
            logger.error(f"Failed to search users: {e}")
            raise

    @classmethod
    def groups_list(cls, system_mgmt_client: SystemMgmt, query_params: Optional[Dict[str, Any]]) -> Any:
        """用户组列表
        
        Args:
            system_mgmt_client: 系统管理客户端
            query_params: 查询参数，可为None
            
        Returns:
            用户组数据
        """
        if not system_mgmt_client:
            logger.error("SystemMgmt client is None")
            raise ValueError("SystemMgmt client cannot be None")

        # 使用常量替代魔法变量
        if query_params is None:
            query_params = cls.DEFAULT_QUERY_PARAMS.copy()
            logger.info("Using default query params for groups search")
        
        if not isinstance(query_params, dict):
            logger.error(f"Invalid query_params type: {type(query_params)}")
            raise TypeError("query_params must be a dictionary")

        try:
            logger.info(f"Searching groups with params: {query_params}")
            groups = system_mgmt_client.search_groups(query_params)
            
            if not isinstance(groups, dict) or "data" not in groups:
                logger.error(f"Invalid result format from search_groups: {groups}")
                raise ValueError("Invalid response format from search_groups")
                
            groups_data = groups["data"]
            logger.info(f"Successfully retrieved groups data")
            return groups_data
            
        except Exception as e:
            logger.error(f"Failed to search groups: {e}")
            raise

    @classmethod
    def user_groups_list(cls, request) -> Dict[str, Any]:
        """用户组列表
        
        Args:
            request: 请求对象，包含用户信息
            
        Returns:
            包含is_all和group_ids的字典
        """
        if not request:
            logger.error("Request object is None")
            raise ValueError("Request cannot be None")
            
        if not hasattr(request, 'user'):
            logger.error("Request object missing user attribute")
            raise AttributeError("Request must have user attribute")

        try:
            user = request.user
            
            # 安全地获取用户属性
            is_super_admin = getattr(user, 'is_superuser', False)
            user_groups = getattr(user, 'group_list', [])
            
            logger.info(f"Processing user groups for user, is_superuser: {is_super_admin}")
            
            if is_super_admin:
                logger.info("User is super admin, returning all groups access")
                return {"is_all": True, "group_ids": []}
                
            try:
                group_instance = Group()
                group_ids = group_instance.get_user_group_and_subgroup_ids(user_group_list=user_groups)
                
                if not isinstance(group_ids, list):
                    logger.warning(f"Expected list for group_ids, got {type(group_ids)}")
                    group_ids = []
                    
                logger.info(f"Retrieved {len(group_ids)} group IDs for user")
                return {"is_all": False, "group_ids": group_ids}
                
            except Exception as e:
                logger.error(f"Failed to get user group and subgroup IDs: {e}")
                # 返回安全的默认值
                return {"is_all": False, "group_ids": []}
                
        except Exception as e:
            logger.error(f"Failed to process user groups list: {e}")
            raise

    @classmethod
    def get_all_groups(cls, system_mgmt_client: SystemMgmt) -> Any:
        """获取所有用户组
        
        Args:
            system_mgmt_client: 系统管理客户端
            
        Returns:
            所有用户组数据
        """
        if not system_mgmt_client:
            logger.error("SystemMgmt client is None")
            raise ValueError("SystemMgmt client cannot be None")

        try:
            logger.info("Retrieving all groups")
            groups = system_mgmt_client.get_all_groups()
            
            if not isinstance(groups, dict) or "data" not in groups:
                logger.error(f"Invalid result format from get_all_groups: {groups}")
                raise ValueError("Invalid response format from get_all_groups")
                
            groups_data = groups["data"]
            logger.info("Successfully retrieved all groups data")
            return groups_data
            
        except Exception as e:
            logger.error(f"Failed to get all groups: {e}")
            raise
