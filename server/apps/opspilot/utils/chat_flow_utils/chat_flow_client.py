from apps.opspilot.utils.safe_eval import evaluate_condition


class ChatFlowClient(object):
    def __init__(self, instance):
        self.instance = instance
        self.parse_chat_flow_json(instance.json_data)
        self.last_output = None
        self.output_list = []

    @staticmethod
    def parse_chat_flow_json(json_data):
        return [
            {"node_id": 1, "index": 1, "parent_node": 0, "type": "sse"},
            {"node_id": 2, "index": 1, "parent_node": 0, "type": "restful"},
            {
                "node_id": 3,
                "index": 1,
                "parent_node": 0,
                "type": "celery",
                "params": {
                    "message": "",
                    "crontab": {
                        "minute": "0",
                        "hour": "14",
                        "day_of_week": "*",
                        "day_of_month": "10",
                    },
                },
            },
            {
                "node_id": 3,
                "index": 2,
                "parent_node": 1,
                "type": "skill",
                "params": {
                    "skill_id": 1,
                },
            },
            {
                "node_id": 4,
                "index": 3,
                "parent_node": 3,
                "type": "condition",
                "params": {"value": "celery", "operator": "==", "output": "celery"},
            },
        ]

    def eval_condition(self, node_id, condition, value, output=None):
        if output is None:
            output = self.last_output
        result = evaluate_condition(f"data {condition} '{value}'", data=str(output))
        self.output_list.append({"node_id": node_id, "output": result})
        return result

    def run_skill_node(self, node_id, skill_id, message):
        pass
