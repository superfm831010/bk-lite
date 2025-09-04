from apps.log.models.log_group import LogGroup


class LogGroupQueryBuilder:
    """日志分组查询构建器 - 专门处理日志分组与查询的组合逻辑"""

    @staticmethod
    def json_to_logsql_expression(rule_json):
        """将规则JSON转换为VictoriaLogs LogsQL表达式"""
        op_map = {
            "==": lambda f, v: f'{f}:"{v}"',
            "!=": lambda f, v: f'!{f}:"{v}"',
            "contains": lambda f, v: f'{f}:*{v}*',
            "!contains": lambda f, v: f'!{f}:*{v}*',
            "startswith": lambda f, v: f'{f}:{v}*',
            "endswith": lambda f, v: f'{f}:*{v}'
        }

        # 如果不存在规则，返回空字符串
        if not rule_json:
            return ""

        mode = rule_json.get("mode", "AND").upper()
        connector = " AND " if mode == "AND" else " OR "

        expressions = []
        for rule in rule_json.get("conditions", []):
            field = rule["field"]
            op = rule["op"]
            value = rule["value"]
            expr_func = op_map.get(op)
            if expr_func:
                expressions.append(expr_func(field, value))
            else:
                raise ValueError(f"Unsupported operation: {op}")

        if not expressions:
            return ""

        if len(expressions) == 1:
            return expressions[0]
        else:
            return f"({connector.join(expressions)})"

    @staticmethod
    def build_query_with_groups(user_query, log_group_ids):
        """构建包含日志分组规则的查询语句

        Args:
            user_query (str): 用户输入的查询语句
            log_group_ids (list): 日志分组ID列表

        Returns:
            tuple: (final_query, group_info)
                   final_query: 最终查询语句
                   group_info: 使用的分组信息（用于调试和日志）
        """
        if not log_group_ids:
            return user_query, []

        # 获取有效的日志分组
        valid_groups = LogGroupQueryBuilder._get_valid_groups(log_group_ids)

        if not valid_groups:
            return user_query, []

        # 构建分组条件
        group_conditions = LogGroupQueryBuilder._build_group_conditions(valid_groups)

        if not group_conditions:
            return user_query, [{"id": g.id, "name": g.name, "status": "empty_rule"} for g in valid_groups]

        # 组合最终查询
        final_query = LogGroupQueryBuilder._combine_query_and_groups(user_query, group_conditions)

        # 构建分组信息
        group_info = [{"id": g.id, "name": g.name, "status": "applied"} for g in valid_groups]

        return final_query, group_info

    @staticmethod
    def _get_valid_groups(log_group_ids):
        """获取有效的日志分组对象"""
        try:
            return list(LogGroup.objects.filter(id__in=log_group_ids))
        except Exception:
            return []

    @staticmethod
    def _build_group_conditions(groups):
        """构建日志分组的查询条件"""
        conditions = []

        for group in groups:
            if not group.rule:
                continue

            try:
                condition = LogGroupQueryBuilder.json_to_logsql_expression(group.rule)
                if condition:  # 移除无意义的检查，空字符串自然会被过滤
                    conditions.append(condition)
            except Exception:
                # 规则转换失败，跳过该分组
                continue

        return conditions

    @staticmethod
    def _combine_query_and_groups(user_query, group_conditions):
        """组合用户查询和分组条件"""
        # 清理用户查询
        user_query = user_query.strip() if user_query else ""

        # 将多个日志分组规则用 OR 连接
        if len(group_conditions) > 1:
            group_filter = f"({' OR '.join(group_conditions)})"
        elif len(group_conditions) == 1:
            group_filter = group_conditions[0]
        else:
            group_filter = ""

        # 组合逻辑
        if user_query and group_filter:
            # 用户有查询 + 有分组条件：AND 连接
            return f"({user_query}) AND ({group_filter})"
        elif group_filter:
            # 无用户查询 + 有分组条件：只使用分组条件
            return group_filter
        elif user_query:
            # 有用户查询 + 无分组条件：只使用用户查询
            return user_query
        else:
            # 无查询无分组：返回空查询（VictoriaLogs会返回所有日志）
            return ""

    @staticmethod
    def validate_log_groups(log_group_ids):
        """验证日志分组是否存在且有效

        Args:
            log_group_ids (list): 日志分组ID列表

        Returns:
            tuple: (is_valid, error_message, valid_groups)
        """
        if not log_group_ids:
            return True, "", []

        if not isinstance(log_group_ids, list):
            return False, "log_groups 必须是一个数组", []

        try:
            existing_groups = list(LogGroup.objects.filter(id__in=log_group_ids))
            existing_ids = {g.id for g in existing_groups}

            # 检查是否有不存在的分组ID
            missing_ids = set(log_group_ids) - existing_ids
            if missing_ids:
                return False, f"以下日志分组不存在: {', '.join(missing_ids)}", existing_groups

            return True, "", existing_groups

        except Exception as e:
            return False, f"查询日志分组时发生错误: {str(e)}", []
