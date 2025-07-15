from typing import Dict, Any, List
from apps.alerts.models import AggregationRules, CorrelationRules
from apps.alerts.common.rules.alert_rules import load_rules, AlertRulesConfig
from apps.core.logger import alert_logger as logger


class DatabaseRuleManager:
    """数据库规则管理器"""

    def __init__(self, window_size="10min"):
        self.rules_config = None
        self.window_size = window_size
        # 延迟加载规则，避免初始化时的潜在问题

    def load_rules_from_database(self) -> AlertRulesConfig:
        """从数据库加载聚合规则 - 直接返回窗口配置对象"""
        try:
            # 获取所有启用的关联规则
            correlation_rules = self._get_active_correlation_rules()
            
            if not correlation_rules:
                logger.warning("没有找到启用的关联规则")
                return None
            
            # 取第一个关联规则创建配置（单一配置模式）
            correlation_rule = correlation_rules[0]
            
            # 构建规则数据
            rules_data = []
            for corr_rule in correlation_rules:
                for agg_rule in corr_rule.aggregation_rules.filter(is_active=True):
                    rules_data.append({
                        'correlation_rule': corr_rule,
                        'aggregation_rule': agg_rule
                    })
            
            # 创建并返回窗口配置
            return self._create_window_config(correlation_rule.window_type, rules_data)
            
        except Exception as e:
            logger.error(f"从数据库加载规则失败: {str(e)}")
            return None

    @staticmethod
    def _get_active_correlation_rules():
        """获取所有启用的关联规则及其聚合规则"""
        instances = CorrelationRules.objects.filter(
            aggregation_rules__is_active=True
        ).prefetch_related('aggregation_rules').distinct()
        return instances

    def load_specific_correlation_rules(self, correlation_rules: List[CorrelationRules]) -> AlertRulesConfig| None:
        """
        加载特定关联规则的配置 - 直接返回窗口配置对象
        
        Args:
            correlation_rules: 要加载的关联规则列表
            
        Returns:
            AlertRulesConfig: 窗口配置对象，如果没有规则则返回None
        """
        try:
            if not correlation_rules:
                logger.warning("没有提供关联规则")
                return None
            
            # 构建规则数据
            rules_data = []
            for correlation_rule in correlation_rules:
                # 只处理启用的聚合规则
                active_aggregation_rules = correlation_rule.aggregation_rules.filter(is_active=True)
                
                for agg_rule in active_aggregation_rules:
                    rules_data.append({
                        'correlation_rule': correlation_rule,
                        'aggregation_rule': agg_rule
                    })
            
            if not rules_data:
                logger.warning("没有找到启用的聚合规则")
                return None
            
            # 使用第一个关联规则的窗口类型作为配置基准
            window_type = correlation_rules[0].window_type
            
            # 创建并返回窗口配置
            config = self._create_window_config(window_type, rules_data)
            logger.info(f"成功加载特定关联规则配置: 窗口类型={window_type}, 规则数={len(rules_data)}")
            
            return config
            
        except Exception as e:
            logger.error(f"加载特定关联规则失败: {str(e)}")
            return None

    def get_correlation_rules(self, correlation_rules) -> Dict[str, List]:
        """按窗口类型分组关联规则"""
        rules_by_window = {}
        
        for correlation_rule in correlation_rules:
            window_type = correlation_rule.window_type
            if window_type not in rules_by_window:
                rules_by_window[window_type] = []
            rules_by_window[window_type].append(correlation_rule)
        
        return rules_by_window

    def _create_window_config(self, window_type: str, rules_data: List) -> AlertRulesConfig:
        """为特定窗口类型创建配置"""
        if not rules_data:
            return AlertRulesConfig(
                window_type=window_type,
                rules=[]
            )

        # 取第一个关联规则的窗口配置作为基准
        base_correlation_rule = rules_data[0]['correlation_rule']

        # 转换聚合规则为规则配置
        rules_list = []
        for rule_data in rules_data:
            try:
                agg_rule = rule_data['aggregation_rule']
                rule_dict = {
                    "rule_id": agg_rule.rule_id,
                    "name": agg_rule.name,
                    "description": agg_rule.description or "",
                    "severity": agg_rule.severity,
                    "is_active": agg_rule.is_active,
                    "title": agg_rule.template_title or "",
                    "content": agg_rule.template_content or "",
                    "condition": self._parse_rule_condition(agg_rule.condition)
                }
                rules_list.append(rule_dict)
                logger.debug(f"成功转换规则: {agg_rule.name}")
            except Exception as e:
                logger.error(f"转换规则失败: {str(e)}")
                continue

        from apps.alerts.common.rules.alert_rules import AlertRuleConfig
        rules = [AlertRuleConfig(**rule_dict) for rule_dict in rules_list]
        return AlertRulesConfig(
            window_size=base_correlation_rule.window_size,
            window_type=window_type,
            alignment=base_correlation_rule.alignment,
            max_window_size=base_correlation_rule.max_window_size or "1h",
            session_timeout=base_correlation_rule.session_timeout or "30m",
            session_key_fields=base_correlation_rule.session_key_fields,
            rules=rules
        )

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
            'aggregation_key': data.get('aggregation_key', ['resource_id']),
            'session_close': data.get('session_close', {})
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
