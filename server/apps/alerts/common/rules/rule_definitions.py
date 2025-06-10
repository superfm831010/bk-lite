# -- coding: utf-8 --
from typing import List
from apps.alerts.common.rules.base import BaseRuleSet, AlertRule, RuleCondition, SeverityLevel, ConditionType


class SystemMonitorRules(BaseRuleSet):
    """系统监控规则集"""
    
    @property
    def window_size(self) -> str:
        return "10min"
    
    def get_rules(self) -> List[AlertRule]:
        return [
            # CPU使用率告警
            AlertRule(
                name="high_cpu",
                description="CPU使用率超过85%",
                severity=SeverityLevel.WARNING,
                condition=RuleCondition(
                    type=ConditionType.THRESHOLD,
                    field="cpu_usage",
                    threshold=85.0,
                    operator=">="
                )
            ),
            
            # CPU持续高使用率
            AlertRule(
                name="sustained_high_cpu",
                description="CPU连续3个周期使用率超过80%",
                severity=SeverityLevel.WARNING,
                condition=RuleCondition(
                    type=ConditionType.SUSTAINED,
                    field="cpu_usage",
                    threshold=80.0,
                    operator=">=",
                    required_consecutive=3
                )
            ),
            
            # 磁盘IO延迟
            AlertRule(
                name="disk_io_latency_spike",
                description="磁盘IO延迟大于5.0",
                severity=SeverityLevel.SEVERITY,
                condition=RuleCondition(
                    type=ConditionType.THRESHOLD,
                    field="disk_io_latency",
                    threshold=5.0,
                    operator=">"
                )
            ),
            
            # CPU使用率突增
            AlertRule(
                name="cpu_trend_spike",
                description="CPU使用率突增超过20%",
                severity=SeverityLevel.FATAL,
                condition=RuleCondition(
                    type=ConditionType.TREND,
                    field="cpu_usage",
                    threshold=20.0,
                    operator=">",
                    baseline_window=5,
                    trend_method="percentage"
                )
            ),
        ]


class ApplicationRules(BaseRuleSet):
    """应用监控规则集"""
    
    @property
    def window_size(self) -> str:
        return "10min"
    
    def get_rules(self) -> List[AlertRule]:
        return [
            # 前置状态检查
            AlertRule(
                name="prev_status_equals",
                description="当同一source、obj、obj_inst, metric的上一条event状态为close且本次满足条件时，创建alert并关联",
                severity=SeverityLevel.FATAL,
                condition=RuleCondition(
                    type=ConditionType.PREV_FIELD,
                    field="",
                    group_by=["source_id", "resource_type", "resource_id", "item"],
                    prev_status_field="status",
                    prev_status_value="closed"
                )
            ),
        ]


class JenkinsRules(BaseRuleSet):
    """Jenkins监控规则集"""
    
    @property
    def window_size(self) -> str:
        return "10min"
    
    def get_rules(self) -> List[AlertRule]:
        return [
            # Jenkins单次构建失败
            AlertRule(
                name="jenkins_single_failure",
                description="Jenkins单次构建失败",
                severity=SeverityLevel.WARNING,
                title="Jenkins构建失败 - ${resource_name}",
                content="流水线: ${resource_name}\n状态: 构建失败\n构建号: ${value}\n错误信息: ${description}",
                condition=RuleCondition(
                    type=ConditionType.THRESHOLD,
                    field="build_status",
                    threshold=0.0,
                    operator="=="
                )
            ),
            
            # Jenkins连续构建失败
            AlertRule(
                name="jenkins_sustained_failures",
                description="Jenkins构建连续失败3次",
                severity=SeverityLevel.FATAL,
                title="Jenkins流水线 ${resource_name} 连续构建失败",
                content="流水线: ${resource_name}\n连续失败次数: 3次",
                condition=RuleCondition(
                    type=ConditionType.SUSTAINED,
                    field="build_status",
                    threshold=0.0,
                    operator="==",
                    required_consecutive=3,
                    group_by=["resource_id"]
                )
            ),
        ]


class DefaultRuleSet(BaseRuleSet):
    """默认规则集，包含所有规则"""
    
    @property
    def window_size(self) -> str:
        return "10min"
    
    def get_rules(self) -> List[AlertRule]:
        all_rules = []
        rule_sets = [
            SystemMonitorRules(),
            ApplicationRules(),
            JenkinsRules(),
        ]
        
        for rule_set in rule_sets:
            all_rules.extend(rule_set.get_rules())
        
        return all_rules
