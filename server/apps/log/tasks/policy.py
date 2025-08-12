import uuid
from celery.app import shared_task
from datetime import datetime, timezone

from apps.core.exceptions.base_app_exception import BaseAppException
from apps.log.constants import KEYWORD, AGGREGATE, ALERT_STATUS_NEW
from apps.log.models.policy import Policy, Alert, Event, EventRawData
from apps.log.utils.query_log import VictoriaMetricsAPI
from apps.monitor.utils.system_mgmt_api import SystemMgmtUtils
from apps.core.logger import celery_logger as logger


@shared_task
def scan_log_policy_task(policy_id):
    """扫描日志策略"""
    logger.info(f"start to scan log policy, [{policy_id}]")

    try:
        policy_obj = Policy.objects.filter(id=policy_id).select_related("collect_type").first()
        if not policy_obj:
            raise BaseAppException(f"No Policy found with id {policy_id}")

        if policy_obj.enable:
            # 修正时间计算逻辑 - 应该基于当前时间而非累加
            current_time = datetime.now(timezone.utc)
            if not policy_obj.last_run_time:
                policy_obj.last_run_time = current_time

            # 保存当前执行时间
            policy_obj.last_run_time = current_time
            policy_obj.save()

            LogPolicyScan(policy_obj).run()

        logger.info(f"end to scan log policy, [{policy_id}]")
    except Exception as e:
        logger.error(f"scan log policy task failed, policy_id: {policy_id}, error: {e}")
        raise


def period_to_seconds(period):
    """周期转换为秒"""
    if not period:
        raise BaseAppException("policy period is empty")

    period_type = period.get("type")
    period_value = period.get("value")

    if not period_type or period_value is None:
        raise BaseAppException("invalid period format, missing type or value")

    if period_type == "min":
        return period_value * 60
    elif period_type == "hour":
        return period_value * 3600
    elif period_type == "day":
        return period_value * 86400
    else:
        raise BaseAppException(f"invalid period type: {period_type}")


def format_period(period):
    """格式化周期为VictoriaLogs格式"""
    if not period:
        raise BaseAppException("policy period is empty")

    period_type = period.get("type")
    period_value = period.get("value")

    if not period_type or period_value is None:
        raise BaseAppException("invalid period format, missing type or value")

    if period_type == "min":
        return f'{period_value}m'
    elif period_type == "hour":
        return f'{period_value}h'
    elif period_type == "day":
        return f'{period_value}d'
    else:
        raise BaseAppException(f"invalid period type: {period_type}")


class LogPolicyScan:
    def __init__(self, policy):
        self.policy = policy
        self.active_alerts = self.get_active_alerts()
        self.vlogs_api = VictoriaMetricsAPI()

    def get_active_alerts(self):
        """获取策略的活动告警"""
        try:
            qs = Alert.objects.filter(policy_id=self.policy.id, status=ALERT_STATUS_NEW)
            # 如果设置了组织范围，只查询组织范围内的告���
            if self.policy.organizations:
                # 这里假��source_id包含组织信息，实际可能需要根据具���业务逻辑调整
                pass
            return qs
        except Exception as e:
            logger.error(f"get active alerts failed: {e}")
            return Alert.objects.none()

    def keyword_alert_detection(self):
        """关键字告警检测"""
        events = []

        try:
            # 修正时间计算逻辑
            end_timestamp = int(self.policy.last_run_time.timestamp())
            period_seconds = period_to_seconds(self.policy.period)
            start_timestamp = end_timestamp - period_seconds

            # 构建查询条件
            alert_condition = self.policy.alert_condition
            query = alert_condition.get("query", "")

            if not query:
                logger.warning(f"policy {self.policy.id} has empty query for keyword alert")
                return events

            # 查询日志
            logs = self.vlogs_api.query(
                query=query,
                start=start_timestamp,
                end=end_timestamp,
                limit=alert_condition.get("limit", 1000)
            )

            if logs:
                # 关键字告警按策略聚合，所有匹配日志合并到一个告警中
                source_id = f"policy_{self.policy.id}"

                events.append({
                    "source_id": source_id,
                    "level": self.policy.alert_level,
                    "content": f"关键字告警: 检测到 {len(logs)} 条匹配日志",
                    "value": len(logs),
                    "raw_data": logs[:10]  # 只保留前10条日志作为原始数据
                })

        except Exception as e:
            logger.error(f"keyword alert detection failed for policy {self.policy.id}: {e}")

        return events

    def aggregate_alert_detection(self):
        """聚合告警检测"""
        events = []

        try:
            # 修正时间计算逻辑
            end_timestamp = int(self.policy.last_run_time.timestamp())
            period_seconds = period_to_seconds(self.policy.period)
            start_timestamp = end_timestamp - period_seconds

            alert_condition = self.policy.alert_condition
            base_query = alert_condition.get("query", "*")
            group_by = alert_condition.get("group_by", [])
            rule = alert_condition.get("rule", {})

            # 验证必要参数
            if not rule.get("conditions"):
                logger.warning(f"policy {self.policy.id} has no rule conditions for aggregate alert")
                return events

            # 构建LogSQL聚合查询语句
            aggregation_query = self._build_aggregation_query(base_query, group_by, rule)
            logger.info(f"Executing aggregation query for policy {self.policy.id}: {aggregation_query}")

            # 执行聚合查询
            aggregation_results = self.vlogs_api.query(
                query=aggregation_query,
                start=start_timestamp,
                end=end_timestamp,
                limit=1000  # 聚合结果通常数量较少
            )

            if not aggregation_results:
                logger.info(f"No aggregation results for policy {self.policy.id}")
                return events

            # 处理聚合查询结果
            for result in aggregation_results:
                # 从聚合结果中提取计算值
                aggregate_data = self._extract_aggregate_data(result, rule)

                # 检查是否满足告警条件
                if self._check_rule_conditions(aggregate_data, rule):
                    # 构建分组标识和source_id
                    if group_by:
                        # 有分组字段：按策略+聚合字段值生成source_id
                        group_key = self._build_group_key(result, group_by)
                        source_id = f"policy_{self.policy.id}_{group_key}"
                        content_prefix = f"聚合告警({group_key})"
                    else:
                        # 无分组字段：按策略生成source_id
                        source_id = f"policy_{self.policy.id}"
                        content_prefix = "聚合告警(全局)"

                    events.append({
                        "source_id": source_id,
                        "level": self.policy.alert_level,
                        "content": f"{content_prefix}: 触发条件 {self._format_rule_result(aggregate_data, rule)}",
                        "value": aggregate_data.get("count", 0),
                        "raw_data": {"aggregate_result": aggregate_data, "rule": rule, "query_result": result}
                    })

        except Exception as e:
            logger.error(f"aggregate alert detection failed for policy {self.policy.id}: {e}")

        return events

    def _build_aggregation_query(self, base_query, group_by, rule):
        """构建LogSQL聚合查询语句"""
        conditions = rule.get("conditions", [])

        if not conditions:
            raise BaseAppException("rule conditions cannot be empty")

        # 收集需要计算的聚合函数
        stats_functions = []

        for condition in conditions:
            func = condition.get("func")
            field = condition.get("field", "_msg")

            if not func:
                logger.warning(f"condition missing func: {condition}")
                continue

            if func == "count":
                # count函数不需要字段参数，使用别名
                alias = f"count_{field.replace('.', '_')}"  # 处理字段名中的特殊字符
                stats_functions.append(f"count() as {alias}")
            elif func == "sum":
                alias = f"sum_{field.replace('.', '_')}"
                stats_functions.append(f"sum({field}) as {alias}")
            elif func == "avg":
                alias = f"avg_{field.replace('.', '_')}"
                stats_functions.append(f"avg({field}) as {alias}")
            elif func == "max":
                alias = f"max_{field.replace('.', '_')}"
                stats_functions.append(f"max({field}) as {alias}")
            elif func == "min":
                alias = f"min_{field.replace('.', '_')}"
                stats_functions.append(f"min({field}) as {alias}")
            else:
                logger.warning(f"unsupported aggregation function: {func}")

        # 如果没有有效的聚合函数，默认使用count
        if not stats_functions:
            stats_functions.append("count() as total_count")

        # 去重聚合函数
        stats_functions = list(dict.fromkeys(stats_functions))

        # 构建stats子句
        stats_clause = ", ".join(stats_functions)

        # 构建完整查询 - 使用正确的语法顺序
        if group_by:
            # 有分组的情况：query | stats by (field1, field2) func1() as alias1, func2() as alias2
            by_fields = ", ".join(group_by)
            query = f"{base_query} | stats by ({by_fields}) {stats_clause}"
        else:
            # 无分组的情况：query | stats func1() as alias1, func2() as alias2
            query = f"{base_query} | stats {stats_clause}"

        logger.debug(f"Built aggregation query: {query}")
        return query

    def _extract_aggregate_data(self, result, rule):
        """从查询结果中提取聚合数据"""
        aggregate_data = {}
        conditions = rule.get("conditions", [])

        for condition in conditions:
            func = condition.get("func")
            field = condition.get("field", "_msg")

            if not func:
                continue

            # 根据别名格式提取数据
            if func == "count":
                alias = f"count_{field.replace('.', '_')}"
                aggregate_data[f"{func}_{field}"] = result.get(alias, result.get("total_count", 0))
                # 兼容原有逻辑，设置通用的count值
                if "count" not in aggregate_data:
                    aggregate_data["count"] = aggregate_data[f"{func}_{field}"]
            else:
                alias = f"{func}_{field.replace('.', '_')}"
                aggregate_data[f"{func}_{field}"] = result.get(alias, 0)

        return aggregate_data

    def _build_group_key(self, result, group_by):
        """根据分组字段构建分组标识"""
        if not group_by:
            return ""

        group_values = []
        for field in group_by:
            field_value = result.get(field, "unknown")
            group_values.append(f"{field}={field_value}")

        return ", ".join(group_values)

    def _check_rule_conditions(self, aggregate_data, rule):
        """检查规则条件"""
        conditions = rule.get("conditions", [])
        mode = rule.get("mode", "and")

        if not conditions:
            return False

        condition_results = []
        for condition in conditions:
            func = condition.get("func")
            field = condition.get("field", "_msg")
            op = condition.get("op")
            expected_value = condition.get("value")

            if not all([func, op, expected_value is not None]):
                logger.warning(f"incomplete condition: {condition}")
                continue

            # 获取聚合值
            key = f"{func}_{field}"
            if func == "count":
                actual_value = aggregate_data.get("count", aggregate_data.get(key, 0))
            else:
                actual_value = aggregate_data.get(key, 0)

            # 执行条件比较
            comparison_result = self._compare_values(actual_value, op, expected_value)
            condition_results.append(comparison_result)

            logger.debug(f"condition check: {key}={actual_value} {op} {expected_value} -> {comparison_result}")

        if not condition_results:
            return False

        # 根据mode组合结果
        if mode == "and":
            return all(condition_results)
        elif mode == "or":
            return any(condition_results)
        else:
            logger.warning(f"unsupported rule mode: {mode}")
            return False

    def _compare_values(self, actual_value, op, expected_value):
        """比较值"""
        try:
            # 确保数值类型匹配
            if isinstance(expected_value, (int, float)) and isinstance(actual_value, (int, float)):
                if op == ">":
                    return actual_value > expected_value
                elif op == "<":
                    return actual_value < expected_value
                elif op == "=":
                    return actual_value == expected_value
                elif op == "!=":
                    return actual_value != expected_value

            # 字符串和列表操作
            if op == "in":
                if isinstance(expected_value, list):
                    return actual_value in expected_value
                else:
                    return str(expected_value) in str(actual_value)
            elif op == "nin":
                if isinstance(expected_value, list):
                    return actual_value not in expected_value
                else:
                    return str(expected_value) not in str(actual_value)
            else:
                logger.warning(f"Unsupported operator: {op}")
                return False

        except Exception as e:
            logger.error(f"Error comparing values: {actual_value} {op} {expected_value}, error: {e}")
            return False

    def _format_rule_result(self, aggregate_data, rule):
        """格式化规则结果用于显示"""
        conditions = rule.get("conditions", [])
        mode = rule.get("mode", "and")

        condition_results = []
        for condition in conditions:
            func = condition.get("func")
            field = condition.get("field", "_msg")
            op = condition.get("op")
            expected_value = condition.get("value")

            if not all([func, op, expected_value is not None]):
                continue

            key = f"{func}_{field}"
            if func == "count":
                actual_value = aggregate_data.get("count", aggregate_data.get(key, 0))
            else:
                actual_value = aggregate_data.get(key, 0)

            condition_results.append(f"{func}({field})={actual_value} {op} {expected_value}")

        return f" {mode.upper()} ".join(condition_results)

    def create_events(self, events):
        """创建事件 - 优化版本，使用批量操作"""
        if not events:
            return []

        try:
            # 1. 批量查询所有可能存在的活跃告警
            source_ids = [event["source_id"] for event in events]
            existing_alerts_qs = Alert.objects.filter(
                policy_id=self.policy.id,
                source_id__in=source_ids,
                status=ALERT_STATUS_NEW
            )

            # 手动构建映射表，因为source_id不是唯一字段
            # 对于同一个source_id可能有多个告警，我们取最新的一个
            existing_alerts = {}
            for alert in existing_alerts_qs:
                source_id = alert.source_id
                if source_id not in existing_alerts or alert.created_at > existing_alerts[source_id].created_at:
                    existing_alerts[source_id] = alert

            logger.debug(f"Found {len(existing_alerts)} existing alerts for policy {self.policy.id}")

            # 2. 分类处理：需要更新的告警和需要创建的告警
            alerts_to_update = []
            alerts_to_create = []
            create_events = []
            create_raw_data = []

            for event in events:
                event_id = uuid.uuid4().hex
                source_id = event["source_id"]

                if source_id in existing_alerts:
                    # 存在活跃告警，准备更新
                    alert_obj = existing_alerts[source_id]
                    alert_obj.value = event.get("value", alert_obj.value)
                    alert_obj.content = event["content"]
                    alert_obj.level = event["level"]
                    alert_obj.end_event_time = self.policy.last_run_time
                    alerts_to_update.append(alert_obj)
                else:
                    # 不存在活跃告警，准备创建
                    alert_obj = Alert(
                        id=uuid.uuid4().hex,
                        policy=self.policy,
                        source_id=source_id,
                        collect_type=self.policy.collect_type,
                        level=event["level"],
                        value=event.get("value"),
                        content=event["content"],
                        status=ALERT_STATUS_NEW,
                        start_event_time=self.policy.last_run_time,
                        end_event_time=self.policy.last_run_time,
                        operator=""
                    )
                    alerts_to_create.append(alert_obj)
                    # 更新映射表，供后续事件关联使用
                    existing_alerts[source_id] = alert_obj

                # 准备原始数据记录
                if event.get("raw_data"):
                    create_raw_data.append(
                        EventRawData(
                            event_id=event_id,
                            data=event["raw_data"],
                        )
                    )

                # 准备事件记录（使用映射表中的alert_obj）
                create_events.append(
                    Event(
                        id=event_id,
                        policy=self.policy,
                        source_id=source_id,
                        alert=existing_alerts[source_id],
                        event_time=self.policy.last_run_time,
                        value=event.get("value"),
                        level=event["level"],
                        content=event["content"],
                        notice_result=[]
                    )
                )

            # 3. 批量执行数据库操作
            # 批量创建新告警
            if alerts_to_create:
                Alert.objects.bulk_create(alerts_to_create, batch_size=100)
                logger.debug(f"Created {len(alerts_to_create)} new alerts for policy {self.policy.id}")

            # 批量更新现有告警
            if alerts_to_update:
                Alert.objects.bulk_update(
                    alerts_to_update,
                    ['value', 'content', 'level', 'end_event_time'],
                    batch_size=100
                )
                logger.debug(f"Updated {len(alerts_to_update)} existing alerts for policy {self.policy.id}")

            # 批量创建事件记录
            event_objs = Event.objects.bulk_create(create_events, batch_size=200)

            # 批量创建原始数据记录
            if create_raw_data:
                EventRawData.objects.bulk_create(create_raw_data, batch_size=100)

            logger.info(f"Created {len(event_objs)} events for policy {self.policy.id}")
            return event_objs

        except Exception as e:
            logger.error(f"create events failed for policy {self.policy.id}: {e}")
            return []

    def send_notice(self, event_obj):
        """发送通知"""
        if not self.policy.notice_users:
            return False, []

        title = f"日志告警通知：{self.policy.name}"
        content = f"告警内容：{event_obj.content}\n时间：{event_obj.event_time}\n来源：{event_obj.source_id}"

        try:
            result = SystemMgmtUtils.send_msg_with_channel(
                self.policy.notice_type_id, title, content, self.policy.notice_users
            )
            return True, result
        except Exception as e:
            msg = f"send notice failed for policy {self.policy.id}: {e}"
            logger.error(msg)
            result = [{"error": msg}]
            return False, result


    def notice(self, event_objs):
        """通知"""
        if not event_objs or not self.policy.notice:
            return

        try:

            alerts = []

            for event in event_objs:
                # info级别事件不通知
                if event.level == "info":
                    continue
                is_notice, notice_result = self.send_notice(event)
                event.notice_result = notice_result

                if is_notice:
                    alerts.append((event.alert_id, is_notice))

            # 批量更新通知结果
            Event.objects.bulk_update(event_objs, ["notice_result"], batch_size=200)
            logger.info(f"Completed notification for {len(event_objs)} events")

            # 批量更新告警的通知状态
            if alerts:
                Alert.objects.bulk_update([Alert(id=i[0], notice=i[1]) for i in alerts],["notice"], batch_size=200)

        except Exception as e:
            logger.error(f"notice failed for policy {self.policy.id}: {e}")

    def run(self):
        """运行策略扫描"""
        try:
            events = []

            # 根据告警类型进行不同的检测
            if self.policy.alert_type == KEYWORD:
                events = self.keyword_alert_detection()
            elif self.policy.alert_type == AGGREGATE:
                events = self.aggregate_alert_detection()
            else:
                logger.warning(f"Unknown alert type: {self.policy.alert_type} for policy {self.policy.id}")
                return

            if not events:
                logger.info(f"No alert events detected for policy {self.policy.id}")
                return

            logger.info(f"Detected {len(events)} alert events for policy {self.policy.id}")

            # 创建事件记录
            event_objs = self.create_events(events)

            # 事件通知
            if self.policy.notice and event_objs:
                self.notice(event_objs)

        except Exception as e:
            logger.error(f"Policy scan failed for policy {self.policy.id}: {e}")
            raise
