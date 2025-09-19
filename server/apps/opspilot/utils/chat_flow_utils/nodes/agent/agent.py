"""
智能体节点
"""
from typing import Any, Dict

import jinja2

from apps.core.logger import opspilot_logger as logger
from apps.opspilot.models import LLMSkill
from apps.opspilot.services.llm_service import llm_service
from apps.opspilot.utils.chat_flow_utils.engine.core.base_executor import BaseNodeExecutor


class AgentNode(BaseNodeExecutor):
    """智能体节点"""

    def __init__(self, variable_manager, workflow_instance=None):
        super().__init__(variable_manager)
        self.workflow_instance = workflow_instance

    def execute(self, node_id: str, node_config: Dict[str, Any], input_data: Dict[str, Any]) -> Dict[str, Any]:
        config = node_config["data"].get("config", {})
        input_key = config.get("inputParams", "last_message")
        output_key = config.get("outputParams", "last_message")
        skill_id = config.get("agent")

        if not skill_id:
            raise ValueError(f"智能体节点 {node_id} 缺少 skill_id 参数")

        skill_obj = LLMSkill.objects.filter(id=skill_id).first()
        if not skill_obj:
            raise ValueError(f"技能 {skill_id} 不存在")

        flow_input = self.variable_manager.get_variable("flow_input")
        # 获取消息内容，支持模板变量
        message = input_data.get(input_key)

        # 处理节点中的 prompt 参数和上传文件
        node_prompt = config.get("prompt", "")
        uploaded_files = config.get("uploadedFiles", [])
        final_skill_prompt = skill_obj.skill_prompt

        # 处理上传的文件内容
        files_content = ""
        if uploaded_files and isinstance(uploaded_files, list):
            file_contents = []
            for file_info in uploaded_files:
                if isinstance(file_info, dict) and "name" in file_info and "content" in file_info:
                    file_name = file_info["name"]
                    file_content = file_info["content"]
                    file_contents.append(file_content)
                    logger.info(f"智能体节点 {node_id}: 加载文件 {file_name}")

            if file_contents:
                contents = "\n".join(file_contents)
                files_content = f"""
### 补充内容:
{contents}

"""

        if node_prompt or files_content:
            try:
                # 准备模板变量上下文 - 只使用全局变量
                template_context = self.variable_manager.get_all_variables()

                # 组合完整的节点prompt
                combined_prompt = ""
                if node_prompt:
                    # 使用 Jinja2 渲染 prompt
                    template = jinja2.Template(node_prompt)
                    rendered_prompt = template.render(**template_context)
                    combined_prompt += rendered_prompt

                # 添加文件内容
                if files_content:
                    combined_prompt += files_content

                # 将组合后的 prompt 追加到技能的 prompt 后面
                final_skill_prompt = f"{skill_obj.skill_prompt}\n{combined_prompt}"

                logger.info(f"智能体节点 {node_id}: 追加了自定义prompt和{len(uploaded_files)}个文件内容")

            except Exception as e:
                logger.error(f"智能体节点 {node_id} prompt渲染失败: {str(e)}")
                # 如果渲染失败，使用原始内容
                combined_prompt = node_prompt + files_content
                final_skill_prompt = f"{skill_obj.skill_prompt}\n{combined_prompt}"

        # 构建LLM调用参数
        llm_params = {
            "llm_model": skill_obj.llm_model_id,
            "skill_prompt": final_skill_prompt,  # 使用处理后的prompt
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
            "user_id": flow_input.get("user_id", "anonymous"),
            "enable_km_route": skill_obj.enable_km_route,
            "km_llm_model": skill_obj.km_llm_model,
            "enable_suggest": skill_obj.enable_suggest,
        }

        data, _, _ = llm_service.invoke_chat(llm_params)
        result = data["message"]

        logger.info(f"智能体节点 {node_id} 执行完成，输出长度: {len(result)}")
        return {output_key: result}


# 向后兼容的别名
AgentsNode = AgentNode
