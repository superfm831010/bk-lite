import requests

from apps.opspilot.models import BotWorkFlow, LLMSkill
from apps.opspilot.services.llm_service import llm_service
from apps.opspilot.utils.safe_eval import evaluate_condition


class ChatFlowClient(object):
    def __init__(self, instance: BotWorkFlow, run_type="openai"):
        self.instance = instance

        self.last_output = None
        self.output_data = {}
        self.run_type = run_type
        self.fun_map = {"condition": self.eval_condition, "agents": self.run_skill_node, "http": self.run_http_node}

    @staticmethod
    def parse_chat_flow_json(web_json):
        """
        解析前端流程图JSON数据，转换为后端执行节点列表

        Args:
            web_json: 前端流程图JSON数据，包含nodes和edges

        Returns:
            list: 转换后的节点列表，包含node_id、index、parent_node、type等字段
        """
        if not web_json or "nodes" not in web_json or "edges" not in web_json:
            return []

        nodes = web_json["nodes"]
        edges = web_json["edges"]

        # 构建父子关系映射，支持多个父节点，直接使用原始ID
        parent_map = {}
        for edge in edges:
            source_id = edge["source"]
            target_id = edge["target"]
            if target_id not in parent_map:
                parent_map[target_id] = []
            parent_map[target_id].append(source_id)

        # 转换节点类型映射
        # type_mapping = {
        #     'timeTrigger': 'celery',
        #     'restfulApi': 'restful',
        #     'openaiApi': 'openai',
        #     'agents': 'agents',
        #     'ifCondition': 'condition',
        #     'httpRequest': 'http'
        # }

        result = []
        for node in nodes:
            node_id = node["id"]
            node_type = node["type"]
            # mapped_type = type_mapping.get(node_type, node_type)
            parent_nodes = parent_map.get(node_id, [])

            # 构建基础节点数据
            node_data = {"node_id": node_id, "parent_node": parent_nodes, "type": node_type}

            # 根据节点类型添加特定参数
            config = node.get("data", {}).get("config", {})
            if node_type == "celery" and config:
                # 定时触发器参数
                frequency = config.get("frequency", "daily")
                time_str = config.get("time", "06:00")
                message = config.get("message", "")

                # 解析时间字符串 "HH:MM" 格式
                try:
                    hour, minute = time_str.split(":")
                    hour = int(hour)
                    minute = int(minute)
                except (ValueError, AttributeError):
                    hour, minute = 6, 0  # 默认值

                # 根据频率类型生成crontab配置
                if frequency == "daily":
                    # 每日执行
                    crontab = {
                        "minute": str(minute),
                        "hour": str(hour),
                        "day_of_week": "*",
                        "day_of_month": "*",
                    }
                elif frequency == "weekly":
                    # 每周执行
                    weekday = config.get("weekday", 1)  # 默认周一
                    crontab = {
                        "minute": str(minute),
                        "hour": str(hour),
                        "day_of_week": str(weekday),
                        "day_of_month": "*",
                    }
                else:
                    # 每月执行
                    day = config.get("day", 1)  # 默认每月1号
                    crontab = {
                        "minute": str(minute),
                        "hour": str(hour),
                        "day_of_week": "*",
                        "day_of_month": str(day),
                    }

                node_data["params"] = {"message": message, "crontab": crontab}
            elif node_type == "agents" and config:
                # 智能体参数
                node_data["params"] = {
                    "skill_id": config.get("skill_id"),  # 默认技能ID，可根据agent配置调整
                }
            elif node_type == "condition" and config:
                # 条件分支参数
                field = config.get("conditionField", "")
                operator = config.get("conditionOperator", "==")
                value = config.get("conditionValue", "")
                if field == "triggerType":
                    field = "run_type"

                # 操作符映射
                operator_map = {"equals": "==", "notEquals": "!=", "greaterThan": ">", "lessThan": "<"}
                mapped_operator = operator_map.get(operator, operator)

                node_data["params"] = {"field": field, "operator": mapped_operator, "value": value}
            elif node_type == "http" and config:
                # HTTP请求参数
                node_data["params"] = {"method": config.get("method", "GET"), "url": config.get("url", ""), "timeout": config.get("timeout", 10)}

            result.append(node_data)

        return result

    def run_next_node(self, node_id=0, message=""):
        if node_id == 0:
            node_obj = [i for i in self.instance.flow_json if not i["parent_node"] and i["type"] == self.run_type]
        else:
            node_obj = [i for i in self.instance.flow_json if node_id in i["parent_node"]]
        if not node_obj:
            return
        node_obj = node_obj[0]
        node_type = node_obj["type"]

        fun = self.fun_map.get(node_type)
        fun(node_obj, message)
        self.run_next_node(node_obj["node_id"], self.last_output)

    def eval_condition(self, node_obj, message):
        node_id = node_obj["node_id"]
        condition = node_obj["params"].get("operator", "==")
        value = node_obj["params"].get("value", "")
        field = node_obj["params"].get("field", "run_type")
        if field == "run_type":
            output = self.run_type
        else:
            output = message
        result = evaluate_condition(f"data {condition} '{value}'", data=str(output))
        self.output_data[node_id] = result
        self.last_output = result

    def run_skill_node(self, node_obj, message):
        skill_obj = LLMSkill.objects.filter(id=node_obj["params"].get("skill_id")).first()
        if not skill_obj:
            result = "技能不存在"
            self.last_output = result
            self.output_data[node_obj["node_id"]] = result
            return
        params = {
            "llm_model": skill_obj.llm_model_id,
            "skill_prompt": skill_obj.skill_prompt,
            "temperature": skill_obj.temperature,
            "chat_history": [{"event": "user", "message": message}],
            "user_message": message,
            "conversation_window_size": skill_obj.conversation_window_size,
            "enable_rag": skill_obj.enable_rag,
            "rag_score_threshold": [{"knowledge_base": int(key), "score": float(value)} for key, value in skill_obj.rag_score_threshold_map.items()],
            "enable_rag_knowledge_source": skill_obj.enable_rag_knowledge_source,
            "show_think": skill_obj.show_think,
            "tools": skill_obj.tools,
            "skill_type": skill_obj.skill_type,
            "group": skill_obj.team[0],
            "user_id": self.instance.bot.created_by,
            "enable_km_route": skill_obj.enable_km_route,
            "km_llm_model": skill_obj.km_llm_model,
            "enable_suggest": skill_obj.enable_suggest,
        }
        data, _, _ = llm_service.invoke_chat(params)
        result = data["message"]
        self.last_output = result
        self.output_data[node_obj["node_id"]] = result

    def run_http_node(self, node_obj, message):
        """
        执行HTTP请求节点

        Args:
            node_obj: 节点对象，包含node_id和params配置
            message: 输入消息

        Returns:
            str: HTTP请求的响应结果
        """

        node_id = node_obj["node_id"]
        params = node_obj.get("params", {})

        method = params.get("method", "GET").upper()
        url = params.get("url", "")
        timeout = params.get("timeout", 10)

        if not url:
            result = "HTTP请求失败：URL为空"
            self.last_output = result
            self.output_data[node_id] = result
            return

        try:
            # 根据HTTP方法发送请求
            if method == "GET":
                response = requests.get(url, timeout=timeout)
            elif method == "POST":
                response = requests.post(url, json={"message": message}, timeout=timeout)
            elif method == "PUT":
                response = requests.put(url, json={"message": message}, timeout=timeout)
            elif method == "DELETE":
                response = requests.delete(url, timeout=timeout)
            else:
                result = f"HTTP请求失败：不支持的请求方法 {method}"
                self.last_output = result
                self.output_data[node_id] = result
                return
            # 检查响应状态
            response.raise_for_status()
            # 尝试解析JSON响应，失败则返回文本
            try:
                result = response.json()
            except ValueError:
                result = response.text

        except requests.exceptions.Timeout:
            result = f"HTTP请求超时：{url}"
        except requests.exceptions.RequestException as e:
            result = f"HTTP请求失败：{str(e)}"
        except Exception as e:
            result = f"HTTP请求异常：{str(e)}"

        self.last_output = result
        self.output_data[node_id] = result
