# -- coding: utf-8 --
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from apps.alerts.common.rules.alert_rules import AlertRuleConfig
from apps.alerts.common.aggregation.alert_engine import RuleEngine
from apps.alerts.services.rule_manager import DatabaseRuleManager
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
        self.rules_config = None
        self.engine = None
        # 延迟初始化，在第一次使用时加载

    def _init_engine(self):
        """初始化规则引擎"""
        try:
            # 加载所有规则到引擎
            for rule in self.rules_config.rules:
                self.engine.add_rule(rule.dict())

            logger.info(f"Rule manager initialized with {len(self.rules_config.rules)} rules")
        except Exception as e:
            logger.error(f"Failed to initialize rule engine: {e}")
            raise

    def _ensure_initialized(self):
        """确保规则管理器已初始化"""
        if self.rules_config is None or self.engine is None:
            self.initialize_with_database_rules()

    def get_active_rules(self) -> List[AlertRuleConfig]:
        """获取所有激活的规则"""
        return [rule for rule in self.rules_config.rules if rule.is_active]

    def get_rule_by_id(self, rule_id: str) -> Optional[AlertRuleConfig]:
        """根据名称获取规则"""
        for rule in self.rules_config.rules:
            if rule.rule_id == rule_id:
                return rule
        return None

    def add_rule(self, rule_config: Dict[str, Any]) -> bool:
        """添加新规则"""
        try:
            # 验证规则配置
            rule = AlertRuleConfig(**rule_config)

            # 添加到规则列表
            self.rules_config.rules.append(rule)

            # 添加到引擎
            self.engine.add_rule(rule_config)

            logger.info(f"Added new rule: {rule.name}")
            return True
        except Exception as e:
            logger.error(f"Failed to add rule: {e}")
            return False

    def update_rule(self, rule_name: str, rule_config: Dict[str, Any]) -> bool:
        """更新规则"""
        try:
            # 找到并更新规则
            for i, rule in enumerate(self.rules_config.rules):
                if rule.name == rule_name:
                    updated_rule = AlertRuleConfig(**rule_config)
                    self.rules_config.rules[i] = updated_rule

                    # 重新初始化引擎
                    self._init_engine()

                    logger.info(f"Updated rule: {rule_name}")
                    return True

            logger.warning(f"Rule not found: {rule_name}")
            return False
        except Exception as e:
            logger.error(f"Failed to update rule {rule_name}: {e}")
            return False

    def remove_rule(self, rule_name: str) -> bool:
        """删除规则"""
        try:
            # 找到并删除规则
            for i, rule in enumerate(self.rules_config.rules):
                if rule.name == rule_name:
                    del self.rules_config.rules[i]

                    # 重新初始化引擎
                    self._init_engine()

                    logger.info(f"Removed rule: {rule_name}")
                    return True

            logger.warning(f"Rule not found: {rule_name}")
            return False
        except Exception as e:
            logger.error(f"Failed to remove rule {rule_name}: {e}")
            return False

    def execute_rules(self, events_df) -> Dict[str, RuleExecutionResult]:
        """执行所有规则"""
        if not self.rules_config or not self.rules_config.rules:
            logger.error("No rules available to execute")
            return {}

        if not self.engine:
            logger.error("Rule engine not initialized")
            return {}

        try:
            logger.info(f"开始执行规则，共有 {len(self.rules_config.rules)} 条规则")
            results = self.engine.process_events(events_df)

            # 转换为RuleExecutionResult格式
            execution_results = {}
            for rule_name, result in results.items():
                execution_results[rule_name] = RuleExecutionResult(
                    rule_name=rule_name,
                    triggered=result['triggered'],
                    instances=result.get('instances', {}),
                    description=result.get('description', ''),
                    severity=result.get('severity', 'warning'),
                    source_name=result.get('source_name', '')
                )

            logger.info(f"规则执行完成，触发 {len([r for r in execution_results.values() if r.triggered])} 条规则")
            return execution_results

        except Exception as e:
            logger.error(f"Failed to execute rules: {e}")
            return {}

    def get_rule_statistics(self) -> Dict[str, Any]:
        """获取规则统计信息"""
        active_rules = self.get_active_rules()
        return {
            'total_rules': len(self.rules_config.rules),
            'active_rules': len(active_rules),
            'inactive_rules': len(self.rules_config.rules) - len(active_rules),
            'rule_types': self._get_rule_type_stats(),
            'severity_distribution': self._get_severity_stats()
        }

    def _get_rule_type_stats(self) -> Dict[str, int]:
        """获取规则类型统计"""
        type_stats = {}
        for rule in self.rules_config.rules:
            rule_type = rule.condition.type
            type_stats[rule_type] = type_stats.get(rule_type, 0) + 1
        return type_stats

    def _get_severity_stats(self) -> Dict[str, int]:
        """获取严重级别统计"""
        severity_stats = {}
        for rule in self.rules_config.rules:
            severity = rule.severity
            severity_stats[severity] = severity_stats.get(severity, 0) + 1
        return severity_stats

    def reload_rules(self):
        """重新加载规则"""
        try:
            # 可以从数据库或配置文件重新加载规则
            # 这里暂时使用默认规则
            self.rules_config = self.db_rule_manager.load_rules_from_database()
            self._init_engine()
            logger.info("Rules reloaded successfully")
        except Exception as e:
            logger.error(f"Failed to reload rules: {e}")
            raise

    def reload_rules_from_database(self):
        """从数据库重新加载规则"""
        try:
            logger.info("开始从数据库重新加载规则")
            self.rules_config = self.db_rule_manager.load_rules_from_database()

            if self.rules_config and self.rules_config.rules:
                self.engine = RuleEngine(window_size=self.rules_config.window_size)
                self._init_engine()
                logger.info(f"成功从数据库重新加载 {len(self.rules_config.rules)} 条规则")
            else:
                logger.warning("从数据库加载的规则为空")

        except Exception as e:
            logger.error(f"从数据库重新加载规则失败: {str(e)}")
            raise

    def initialize_with_database_rules(self):
        """使用数据库规则初始化"""
        logger.info("开始使用数据库规则初始化规则管理器")
        self.rules_config = self.db_rule_manager.load_rules_from_database()

        if self.rules_config:
            self.engine = RuleEngine(window_size=self.rules_config.window_size)
            self._init_engine()
            logger.info("规则管理器初始化完成")
        else:
            logger.error("规则管理器初始化失败：无法加载规则配置")


# 延迟初始化全局实例
_rule_manager_instance = None


def get_rule_manager(window_size="10min") -> RuleManager:
    """获取规则管理器实例（支持数据库规则）"""
    global _rule_manager_instance
    if _rule_manager_instance is None:
        _rule_manager_instance = RuleManager(window_size=window_size)
        logger.info("规则管理器实例已创建")
    return _rule_manager_instance
