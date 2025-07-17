class StreamUtils:

    @staticmethod
    def json_to_jq_expression(rule_json):
        op_map = {
            "==": lambda f, v: f'.{f} == "{v}"',
            "!=": lambda f, v: f'.{f} != "{v}"',
            "contains": lambda f, v: f'.{f} | contains("{v}")',
            "!contains": lambda f, v: f'(.{f} | contains("{v}")) | not',
            "startswith": lambda f, v: f'.{f} | startswith("{v}")',
            "endswith": lambda f, v: f'.{f} | endswith("{v}")'
        }

        mode = rule_json.get("mode", "AND").upper()
        connector = " and " if mode == "AND" else " or "

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

        return connector.join(f"({e})" for e in expressions)
