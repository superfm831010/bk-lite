# -- coding: utf-8 --
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from apps.alerts.common.rules.alert_rules import AlertRuleConfig
from apps.alerts.common.aggregation.alert_engine import RuleEngine
from apps.alerts.common.rules.db_rule_manager import DatabaseRuleManager
from apps.core.logger import alert_logger as logger


@dataclass
class RuleExecutionResult:
    """规则执行结果"""
    rule_name: str
    triggered: bool
    instances: Dict[str, Any]
    description: str
    severity: str
    source_name: str


class RuleManager:
    """告警规则管理器"""

    def __init__(self, window_size="10min"):
        self.window_size = window_size
        self.db_rule_manager = DatabaseRuleManager(window_size=self.window_size)
        self.window_config = None  # 存储单个窗口配置
        self.engine = None  # 存储单个引擎
        self._initialized = False  # 初始化状态标记
        # 延迟初始化，在第一次使用时加载

    def _init_engine(self):
        """初始化规则引擎"""
        try:
            if self.window_config and self.window_config.rules:
                # 创建单个引擎
                self.engine = RuleEngine(window_size=self.window_config.window_size)

                # 加载所有规则
                for rule in self.window_config.rules:
                    self.engine.add_rule(rule.dict())

                logger.info(
                    f"初始化 {self.window_config.window_type} 窗口类型引擎，包含 {len(self.window_config.rules)} 条规则")
            else:
                logger.warning("没有可用的窗口配置或规则")

        except Exception as e:
            logger.error(f"初始化规则引擎失败: {e}")
            raise

    def _ensure_initialized(self):
        """确保规则管理器已初始化"""
        if not self.window_config or not self.engine or not self._initialized:
            self.initialize_with_database_rules()

    def get_active_rules(self) -> List[AlertRuleConfig]:
        """获取所有激活的规则"""
        if not self.window_config:
            return []
        return [rule for rule in self.window_config.rules if rule.is_active]

    def get_rule_by_id(self, rule_id: str) -> Optional[AlertRuleConfig]:
        """根据名称获取规则"""
        if not self.window_config:
            return None
        for rule in self.window_config.rules:
            if rule.rule_id == rule_id:
                return rule
        return None

    def get_window_types(self) -> List[str]:
        """获取当前窗口类型"""
        self._ensure_initialized()
        return [self.window_config.window_type] if self.window_config else []

    def get_config_by_window_type(self, window_type: str):
        """根据窗口类型获取配置"""
        self._ensure_initialized()
        if self.window_config and self.window_config.window_type == window_type:
            return self.window_config
        return None

    def add_rule(self, rule_config: Dict[str, Any]) -> bool:
        """添加新规则"""
        try:
            # 验证规则配置
            rule = AlertRuleConfig(**rule_config)

            if not self.window_config:
                logger.error("窗口配置未初始化，无法添加规则")
                return False

            # 添加到规则列表
            self.window_config.rules.append(rule)

            # 添加到引擎
            if self.engine:
                self.engine.add_rule(rule_config)

            logger.info(f"成功添加规则: {rule.name}")
            return True
        except Exception as e:
            logger.error(f"添加规则失败: {e}")
            return False

    def update_rule(self, rule_name: str, rule_config: Dict[str, Any]) -> bool:
        """更新规则"""
        try:
            if not self.window_config:
                logger.warning("窗口配置未初始化")
                return False

            # 找到并更新规则
            for i, rule in enumerate(self.window_config.rules):
                if rule.name == rule_name:
                    updated_rule = AlertRuleConfig(**rule_config)
                    self.window_config.rules[i] = updated_rule

                    # 重新初始化引擎
                    self._init_engine()

                    logger.info(f"更新规则成功: {rule_name}")
                    return True

            logger.warning(f"未找到规则: {rule_name}")
            return False
        except Exception as e:
            logger.error(f"更新规则失败 {rule_name}: {e}")
            return False

    def remove_rule(self, rule_name: str) -> bool:
        """删除规则"""
        try:
            if not self.window_config:
                logger.warning("窗口配置未初始化")
                return False

            # 找到并删除规则
            for i, rule in enumerate(self.window_config.rules):
                if rule.name == rule_name:
                    del self.window_config.rules[i]

                    # 重新初始化引擎
                    self._init_engine()

                    logger.info(f"删除规则成功: {rule_name}")
                    return True

            logger.warning(f"未找到规则: {rule_name}")
            return False
        except Exception as e:
            logger.error(f"删除规则失败 {rule_name}: {e}")
            return False

    def execute_rules(self, events_df) -> Dict[str, RuleExecutionResult]:
        """执行所有规则"""
        if not self.window_config or not self.window_config.rules:
            logger.error("没有可用的规则")
            return {}

        if not self.engine:
            logger.error("规则引擎未初始化")
            return {}

        try:
            logger.info(
                f"开始执行 {self.window_config.window_type} 窗口类型的规则，共有 {len(self.window_config.rules)} 条规则")
            results = self.engine.process_events(events_df)

            # 转换为RuleExecutionResult格式
            formatted_results = {}
            for rule_name, result in results.items():
                formatted_results[rule_name] = RuleExecutionResult(
                    rule_name=rule_name,
                    triggered=result['triggered'],
                    instances=result.get('instances', {}),
                    description=result.get('description', ''),
                    severity=result.get('severity', 'warning'),
                    source_name=result.get('source_name', '')
                )

            logger.info(f"规则执行完成，触发 {len([r for r in formatted_results.values() if r.triggered])} 条规则")
            return formatted_results

        except Exception as e:
            logger.error(f"执行规则失败: {e}")
            return {}

    def get_rule_statistics(self) -> Dict[str, Any]:
        """获取规则统计信息"""
        if not self.window_config:
            return {
                'total_rules': 0,
                'active_rules': 0,
                'inactive_rules': 0,
                'rule_types': {},
                'severity_distribution': {}
            }

        active_rules = self.get_active_rules()
        total_rules = len(self.window_config.rules)

        return {
            'total_rules': total_rules,
            'active_rules': len(active_rules),
            'inactive_rules': total_rules - len(active_rules),
            'rule_types': self._get_rule_type_stats(),
            'severity_distribution': self._get_severity_stats()
        }

    def _get_rule_type_stats(self) -> Dict[str, int]:
        """获取规则类型统计"""
        if not self.window_config:
            return {}

        type_stats = {}
        for rule in self.window_config.rules:
            rule_type = rule.condition.type
            type_stats[rule_type] = type_stats.get(rule_type, 0) + 1
        return type_stats

    def _get_severity_stats(self) -> Dict[str, int]:
        """获取严重级别统计"""
        if not self.window_config:
            return {}

        severity_stats = {}
        for rule in self.window_config.rules:
            severity = rule.severity
            severity_stats[severity] = severity_stats.get(severity, 0) + 1
        return severity_stats

    def reload_rules(self):
        """重新加载规则"""
        try:
            # 直接获取窗口配置对象，不再使用字典包装
            self.window_config = self.db_rule_manager.load_rules_from_database()
            if self.window_config:
                self._init_engine()
                logger.info("规则重新加载成功")
            else:
                logger.warning("没有加载到规则配置")
        except Exception as e:
            logger.error(f"重新加载规则失败: {e}")
            raise

    def reload_rules_from_database(self):
        """从数据库重新加载规则"""
        try:
            logger.info("开始从数据库重新加载规则")
            # 直接获取窗口配置对象，不再使用字典包装
            self.window_config = self.db_rule_manager.load_rules_from_database()

            if self.window_config:
                self._init_engine()
                self._initialized = True
                total_rules = len(self.window_config.rules) if self.window_config else 0
                logger.info(
                    f"成功从数据库重新加载 {total_rules} 条规则，窗口类型: {self.window_config.window_type if self.window_config else 'None'}")
            else:
                logger.warning("从数据库加载的规则为空")

        except Exception as e:
            logger.error(f"从数据库重新加载规则失败: {str(e)}")
            raise

    def initialize_with_database_rules(self):
        """使用数据库规则初始化"""
        logger.info("开始使用数据库规则初始化规则管理器")
        # 直接获取窗口配置对象，不再使用字典包装
        self.window_config = self.db_rule_manager.load_rules_from_database()

        if self.window_config:
            self._init_engine()
            self._initialized = True
            logger.info("规则管理器初始化完成")
        else:
            logger.error("规则管理器初始化失败：无法加载规则配置")

    def get_aggregation_key(self, rule_name: str) -> List[str]:
        """获取聚合键"""
        if not self.window_config:
            logger.error("窗口配置未初始化，无法获取聚合键")
            return []

        for rule in self.window_config.rules:
            if rule.rule_id == rule_name:
                return rule.condition.aggregation_key
        logger.warning(f"未找到规则 {rule_name} 的聚合键")
        return []


# 延迟初始化全局实例
_rule_manager_instance = None


def get_rule_manager(window_size="10min") -> RuleManager:
    """获取规则管理器实例（支持数据库规则）"""
    global _rule_manager_instance
    if _rule_manager_instance is None:
        _rule_manager_instance = RuleManager(window_size=window_size)
        logger.info("规则管理器实例已创建")
    return _rule_manager_instance
