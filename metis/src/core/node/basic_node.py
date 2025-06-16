from typing import TypedDict

import json_repair
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI

from src.core.entity.basic_llm_request import BasicLLMReuqest
from src.rag.naive_rag.elasticsearch.elasticsearch_rag import ElasticSearchRag
from sanic.log import logger


class BasicNode:
    def log(self, config: RunnableConfig, message: str):
        trace_id = config["configurable"]['trace_id']
        logger.debug(f"[{trace_id}] {message}")

    def get_llm_client(self, request: BasicLLMReuqest) -> ChatOpenAI:
        llm = ChatOpenAI(model=request.model, base_url=request.openai_api_base,
                         api_key=request.openai_api_key, temperature=request.temperature)
        return llm

    def prompt_message_node(self, state: TypedDict, config: RunnableConfig) -> TypedDict:
        if config["configurable"]["graph_request"].system_message_prompt:
            state["messages"].append(
                SystemMessage(
                    content=config["configurable"]["graph_request"].system_message_prompt)
            )
        return state

    def add_chat_history_node(self, state: TypedDict, config: RunnableConfig) -> TypedDict:
        if config["configurable"]['graph_request'].chat_history:
            for chat in config["configurable"]['graph_request'].chat_history:
                if chat.event == 'user':
                    if chat.image_data:
                        state['messages'].append(HumanMessage(content=[
                            {"type": "text", "text": "describe the weather in this image"},
                            {"type": "image_url", "image_url": {
                                "url": chat.image_data}},
                        ]))
                    else:
                        state['messages'].append(
                            HumanMessage(content=chat.message))
                elif chat.event == 'assistant':
                    state['messages'].append(AIMessage(content=chat.message))
        return state

    def naive_rag_node(self, state: TypedDict, config: RunnableConfig) -> TypedDict:
        if config["configurable"]['graph_request'].enable_naive_rag is False:
            return state

        naive_rag_request = config["configurable"]["graph_request"].naive_rag_request
        if len(naive_rag_request) == 0:
            return state

        rag_message = f'''
                       以下是参考资料,每份参考资料都由标题和内容组成,以XML格式提供:

                       示例:
                           <knowledge>
                               <ref_id>1</ref_id>
                               <title>知识标题</title>
                               <knowledge_id>1</knowledge_id>
                               <chunk_number>1</chunk_number>
                               <segment_number>2</segment_number>
                               <segment_id>4</segment_id>
                               <content>知识内容</content>
                           </knowledge>

                       字段说明:
                           ref_id: 是第几份参考资料，从1开始
                           title: 参考资料的标题
                           content: 参考资料的内容
                           knowledge_id: 知识id
                           chunk_number: 分块序号
                           chunk_id: 分块ID号
                           segment_number: 分段序号
                           segment_id: 分块ID
                       参考资料:
                   '''

        selected_knowledge_ids = []
        if 'km_info' in config["configurable"]:
            km_info = config["configurable"]["km_info"]
            llm = ChatOpenAI(model=config["configurable"]['km_route_llm_model'],
                             base_url=config["configurable"]['km_route_llm_api_base'],
                             api_key=config["configurable"]['km_route_llm_api_key'],
                             temperature=0.01)

            selected_knowledge_prompt = f"""
                                    我将会给你一段xml，格式为
                                        <knowledge>
                                            <knowledge_id>1</knowledge_id>
                                            <description>知识库描述</description>
                                        <knowledge>
                                    需要根据知识库描述，以及用户的问题，返回与问题相关的知识库id号，格式为json数组，以下是示例: [1,3,2]
                                """
            selected_knowledge_prompt += "任务开始: 以下是需要选择的知识库信息"
            for km in km_info:
                selected_knowledge_prompt += f"""
                            <knowledge>
                                <knowledge_id>{km['index_name']}</knowledge_id>
                                <description>{km['description']}</description>
                            </knowledge>
                        """
            selected_knowledge_prompt += f"请找出与用户问题相关的知识库id号,用户的问题是:{config["configurable"]["graph_request"].user_message}"
            selected_km_response = llm.invoke(selected_knowledge_prompt)
            selected_knowledge_ids = json_repair.loads(
                selected_km_response.content)

        for rag_search_request in naive_rag_request:
            if len(selected_knowledge_ids) != 0 and rag_search_request.index_name not in selected_knowledge_ids:
                logger.info(
                    f"智能知识路由判断:[{rag_search_request.index_name}]不适合当前问题,跳过检索")
            elasticsearch_rag = ElasticSearchRag()
            rag_result = elasticsearch_rag.search(rag_search_request)

            for index, r in enumerate(rag_result):
                rag_message += f"""
                    <knowledge>
                        <ref_id>{index + 1}</ref_id>
                        <title>{r.metadata['_source']['metadata']['knowledge_title']}</title>
                        <knowledge_id>{r.metadata['_source']['metadata']['knowledge_id']}</knowledge_id>
                        <chunk_number>{r.metadata['_source']['metadata']['chunk_number']}</chunk_number>
                        <chunk_id>{r.metadata['_source']['metadata']['chunk_id']}</chunk_id>
                        <segment_number>{r.metadata['_source']['metadata']['segment_number']}</segment_number>
                        <segment_id>{r.metadata['_source']['metadata']['segment_id']}</segment_id>
                        <content>{r.page_content}</content>
                    </knowledge>
                """

            if 'enable_rag_source' in config["configurable"] and config["configurable"]["enable_rag_source"]:
                rag_message += f"""
                在回复中,请使用以下格式返回参考资料的引用:
                    [[1]](ref_id:1|segment_id:1|chunk_id:abc|chunk_number:1|knowledge_id:1|segment_number:1)
                    [[2]]](ref_id:2|segment_id:2|chunk_id:def|chunk_number:2|knowledge_id:0|segment_number:12)

                引用格式说明:
                - 使用数字作为引用标识，简洁明了
                - 使用竖线 | 分隔各个参数
                - 保持参数顺序一致: ref_id|segment_id|chunk_id|chunk_number|knowledge_id|segment_number
                
                在回答内容中的适当位置插入引用链接，格式示例:
                    bklite 是一个AI First的知识管理平台[[1]](ref_id:1|segment_id:1|chunk_id:abc|chunk_number:1|knowledge_id:1|segment_number:1)，致力于帮助用户更高效地获取和管理知识。
                    它的协议是MIT[[2]](ref_id:1|segment_id:1|chunk_id:abc|chunk_number:1|knowledge_id:1|segment_number:1)[[2]](ref_id:2|segment_id:2|chunk_id:def|chunk_number:2|knowledge_id:0|segment_number:12)协议

                注意事项:
                - 每个引用链接都要包含完整的参数信息
                - 引用文本使用简洁的数字标识，如"1"、"2"等
                - 在句子中合适的位置插入引用，不要影响阅读体验
                
                在回复的最后，请添加一个"参考资料"部分,格式如下:
                
                参考资料: 
                    - [1] 知识标题1
                    - [2] 知识标题2
                    - [3] 知识标题3
                
                其中数字与正文中的引用标识保持一致，标题为对应参考资料的title字段内容。
            """

            if 'enable_rag_strict_mode' in config["configurable"] and config["configurable"]["enable_rag_strict_mode"]:
                rag_message += f"""
                        严格按照参考资料的内容进行回答,不允许添加任何额外的内容，不允许捏造任何事实。
                        只允许使用参考资料中的内容进行回答，当参考资料中没有相关内容时，请返回“没有相关内容”。
                """

            state["messages"].append(HumanMessage(content=rag_message))
        return state

    def user_message_node(self, state: TypedDict, config: RunnableConfig) -> TypedDict:
        state["messages"].append(HumanMessage(
            content=config["configurable"]["graph_request"].user_message))
        return state
