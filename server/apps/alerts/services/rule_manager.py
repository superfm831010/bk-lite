from typing import Dict, Any
from apps.alerts.models import AggregationRules
from apps.alerts.common.rules.alert_rules import load_rules, AlertRulesConfig
from apps.core.logger import alert_logger as logger


class DatabaseRuleManager:
    """数据库规则管理器"""

    def __init__(self, window_size="10min"):
        self.rules_config = None
        self.window_size = window_size  # 默认窗口大小
        # 延迟加载规则，避免初始化时的潜在问题

    def load_rules_from_database(self) -> AlertRulesConfig:
        """从数据库加载聚合规则"""
        try:
            aggregation_rules = AggregationRules.objects.filter(is_active=True, correlation_rules__isnull=False)

            if not aggregation_rules.exists():
                logger.warning("数据库中没有找到启用的聚合规则")

            rules_json = self._convert_rules_to_config(self.window_size, aggregation_rules)
            self.rules_config = load_rules(rules_json)
            logger.info(f"成功从数据库加载 {len(aggregation_rules)} 条聚合规则")
            return self.rules_config

        except Exception as e:
            logger.error(f"从数据库加载规则失败: {str(e)}")
            default_config = load_rules({"window_size": "10min", "rules": []})
            self.rules_config = default_config
            return default_config

    def _convert_rules_to_config(self, window_size, aggregation_rules) -> Dict[str, Any]:
        """将AggregationRules转换为规则配置格式"""
        rules_list = []

        for rule in aggregation_rules:
            try:
                rule_dict = {
                    "rule_id": rule.rule_id,
                    "name": rule.name,
                    "description": rule.description or "",
                    "severity": rule.severity,
                    "is_active": rule.is_active,
                    "title": rule.template_title or "",
                    "content": rule.template_content or "",
                    "condition": self._parse_rule_condition(rule.condition)
                }
                rules_list.append(rule_dict)
                logger.debug(f"成功转换规则: {rule.name}")

            except Exception as e:
                logger.error(f"转换规则 {rule.name} 失败: {str(e)}")
                continue

        return {
            "window_size": window_size,
            "rules": rules_list
        }

    def _parse_rule_condition(self, condition_json: list) -> Dict[str, Any]:
        """解析规则条件配置"""
        if not condition_json or not isinstance(condition_json, list):
            logger.warning("规则条件为空或格式不正确")
            return {}

        # 取第一个条件作为主条件
        condition_data = condition_json[0]
        condition_type = condition_data.get("type", "threshold")

        # 基础条件配置
        converted_condition = {
            "type": condition_type,
            "field": condition_data.get("field", ""),
        }

        # 根据条件类型添加特定配置
        if condition_type == "threshold":
            self._add_threshold_config(converted_condition, condition_data)
        elif condition_type == "sustained":
            self._add_sustained_config(converted_condition, condition_data)
        elif condition_type == "trend":
            self._add_trend_config(converted_condition, condition_data)
        elif condition_type == "prev_field_equals":
            self._add_prev_field_config(converted_condition, condition_data)
        elif condition_type == "level_filter":
            self._add_level_filter_config(converted_condition, condition_data)
        elif condition_type == "website_monitoring":
            self._add_website_monitoring_config(converted_condition, condition_data)
        elif condition_type == "filter_and_check":
            self._add_filter_and_check_config(converted_condition, condition_data)

        return converted_condition

    def _add_threshold_config(self, condition: Dict, data: Dict):
        """添加阈值条件配置"""
        condition.update({
            "threshold": data.get("threshold", 0),
            "operator": data.get("operator", ">=")
        })

    def _add_sustained_config(self, condition: Dict, data: Dict):
        """添加持续条件配置"""
        condition.update({
            "threshold": data.get("threshold", 0),
            "operator": data.get("operator", ">="),
            "required_consecutive": data.get("required_consecutive", 3)
        })

    def _add_trend_config(self, condition: Dict, data: Dict):
        """添加趋势条件配置"""
        condition.update({
            "threshold": data.get("threshold", 0),
            "operator": data.get("operator", ">"),
            "baseline_window": data.get("baseline_window", 5),
            "trend_method": data.get("trend_method", "percentage")
        })

    def _add_prev_field_config(self, condition: Dict, data: Dict):
        """添加前置字段条件配置"""
        condition.update({
            "group_by": data.get("group_by", ["source_id", "resource_type", "resource_id", "item"]),
            "prev_status_field": data.get("prev_status_field", "status"),
            "prev_status_value": data.get("prev_status_value", "closed")
        })

    def _add_level_filter_config(self, condition: Dict, data: Dict):
        """添加等级过滤条件配置"""
        condition.update({
            'filter': data.get('filter', {}),
            'target_field': data.get('target_field'),
            'target_field_value': data.get('target_field_value'),
            'target_value_field': data.get('target_value_field', 'value'),
            'target_value': data.get('target_value'),
            'operator': data.get('operator', '=='),
            'aggregation_key': data.get('aggregation_key', ['resource_id'])
        })

    def _add_filter_and_check_config(self, condition: Dict, data: Dict):
        """添加通用过滤检查配置"""
        condition.update({
            'filter': data.get('filter', {}),
            'target_field': data.get('target_field'),
            'target_field_value': data.get('target_field_value'),
            'target_value_field': data.get('target_value_field', 'value'),
            'target_value': data.get('target_value'),
            'operator': data.get('operator', '=='),
            'aggregation_key': data.get('aggregation_key', ['resource_id'])
        })

    def _add_website_monitoring_config(self, condition: Dict, data: Dict):
        """添加网站监控配置（保持向后兼容）"""
        condition.update({
            'filter': data.get('filter', {}),
            'target_field': data.get('target_field'),
            'target_field_value': data.get('target_field_value'),
            'target_value_field': data.get('target_value_field', 'value'),
            'target_value': data.get('target_value'),
            'operator': data.get('operator', '=='),
            'aggregation_key': data.get('aggregation_key', ['resource_id'])
        })
