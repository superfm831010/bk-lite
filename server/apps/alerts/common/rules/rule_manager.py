# -- coding: utf-8 --
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from django.core.cache import cache

from apps.alerts.common.alert_rules import AlertRuleConfig, AlertRulesConfig, VALID_RULES
from apps.alerts.common.alert_engine import RuleEngine

logger = logging.getLogger(__name__)


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
    
    def __init__(self, rules_config: Optional[AlertRulesConfig] = None):
        self.rules_config = rules_config or VALID_RULES
        self.engine = None
        self._cache_key_prefix = "alert_rules"
        self._init_engine()
    
    def _init_engine(self):
        """初始化规则引擎"""
        try:
            self.engine = RuleEngine(
                window_size=self.rules_config.window_size
            )
            
            # 加载所有规则到引擎
            for rule in self.rules_config.rules:
                self.engine.add_rule(rule.dict())
                
            logger.info(f"Rule manager initialized with {len(self.rules_config.rules)} rules")
        except Exception as e:
            logger.error(f"Failed to initialize rule engine: {e}")
            raise
    
    def get_active_rules(self) -> List[AlertRuleConfig]:
        """获取所有激活的规则"""
        return [rule for rule in self.rules_config.rules if rule.is_active]
    
    def get_rule_by_name(self, rule_name: str) -> Optional[AlertRuleConfig]:
        """根据名称获取规则"""
        for rule in self.rules_config.rules:
            if rule.name == rule_name:
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
            
            # 清除缓存
            self._clear_cache()
            
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
                    
                    # 清除缓存
                    self._clear_cache()
                    
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
                    
                    # 清除缓存
                    self._clear_cache()
                    
                    logger.info(f"Removed rule: {rule_name}")
                    return True
            
            logger.warning(f"Rule not found: {rule_name}")
            return False
        except Exception as e:
            logger.error(f"Failed to remove rule {rule_name}: {e}")
            return False
    
    def execute_rules(self, events_df) -> Dict[str, RuleExecutionResult]:
        """执行所有规则"""
        if not self.engine:
            logger.error("Rule engine not initialized")
            return {}
        
        try:
            # 使用引擎处理事件
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
    
    def validate_rule_config(self, rule_config: Dict[str, Any]) -> tuple[bool, str]:
        """验证规则配置"""
        try:
            AlertRuleConfig(**rule_config)
            return True, "Valid"
        except Exception as e:
            return False, str(e)
    
    def reload_rules(self):
        """重新加载规则"""
        try:
            # 可以从数据库或配置文件重新加载规则
            # 这里暂时使用默认规则
            self.rules_config = VALID_RULES
            self._init_engine()
            self._clear_cache()
            logger.info("Rules reloaded successfully")
        except Exception as e:
            logger.error(f"Failed to reload rules: {e}")
            raise
    
    def _clear_cache(self):
        """清除相关缓存"""
        try:
            cache_keys = cache.keys(f"{self._cache_key_prefix}*")
            if cache_keys:
                cache.delete_many(cache_keys)
        except Exception as e:
            logger.warning(f"Failed to clear cache: {e}")


# 全局规则管理器实例
rule_manager = RuleManager()


def get_rule_manager() -> RuleManager:
    """获取规则管理器实例"""
    return rule_manager
