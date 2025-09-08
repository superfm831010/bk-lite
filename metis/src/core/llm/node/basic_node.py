from typing import Dict, Any

import json_repair
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI

from src.core.llm.entity.basic_llm_request import BasicLLMRequest
from src.core.sanic_plus.utils.template_loader import TemplateLoader
from src.core.rag.graph_rag.graphiti.graphiti_rag import GraphitiRAG
from src.core.rag.naive_rag.pgvector.pgvector_rag import PgvectorRag
from sanic.log import logger


class BasicNode:
    def log(self, config: RunnableConfig, message: str):
        trace_id = config["configurable"]['trace_id']
        logger.debug(f"[{trace_id}] {message}")

    def get_llm_client(self, request: BasicLLMRequest, disable_stream=False) -> ChatOpenAI:
        llm = ChatOpenAI(model=request.model, base_url=request.openai_api_base,
                         disable_streaming=disable_stream,
                         api_key=request.openai_api_key, temperature=request.temperature)
        if llm.extra_body is None:
            llm.extra_body = {}

        if disable_stream and 'qwen' in request.model.lower():
            llm.extra_body["enable_thinking"] = False
        return llm

    def prompt_message_node(self, state: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
        system_message_prompt = TemplateLoader.render_template('prompts/graph/base_node_system_message', {
            "user_system_message": config["configurable"]["graph_request"].system_message_prompt
        })

        state["messages"].append(
            SystemMessage(content=system_message_prompt)
        )

        return state

    def suggest_question_node(self, state: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
        if config["configurable"]["graph_request"].enable_suggest:
            suggest_question_prompt = TemplateLoader.render_template(
                'prompts/graph/suggest_question_prompt', {})
            state["messages"].append(SystemMessage(
                content=suggest_question_prompt))
        return state

    def add_chat_history_node(self, state: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
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

    async def naive_rag_node(self, state: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
        naive_rag_request = config["configurable"]["graph_request"].naive_rag_request
        if len(naive_rag_request) == 0:
            return state

        # 智能知识路由选择
        selected_knowledge_ids = []
        if 'km_info' in config["configurable"]:
            selected_knowledge_ids = self._select_knowledge_ids(config)

        rag_result = []

        for rag_search_request in naive_rag_request:
            if len(selected_knowledge_ids) != 0 and rag_search_request.index_name not in selected_knowledge_ids:
                logger.info(
                    f"智能知识路由判断:[{rag_search_request.index_name}]不适合当前问题,跳过检索")
                continue

            rag = PgvectorRag()
            naive_rag_search_result = rag.search(rag_search_request)

            rag_documents = []
            for doc in naive_rag_search_result:
                # 根据 is_doc 字段处理文档内容
                processed_doc = self._process_document_content(doc)
                rag_documents.append(processed_doc)

            rag_result.extend(rag_documents)

            # 执行图谱 RAG 检索
            if rag_search_request.enable_graph_rag:
                graph_results = await self._execute_graph_rag(rag_search_request)
                rag_result.extend(graph_results)

        # 准备模板数据
        template_data = self._prepare_template_data(rag_result, config)

        # 使用模板生成 RAG 消息
        rag_message = TemplateLoader.render_template(
            'prompts/graph/naive_rag_node_prompt', template_data)

        logger.info(f"RAG增强Prompt: {rag_message}")
        state["messages"].append(HumanMessage(content=rag_message))
        return state

    def _select_knowledge_ids(self, config: RunnableConfig) -> list:
        """智能知识路由选择"""
        km_info = config["configurable"]["km_info"]
        llm = ChatOpenAI(model=config["configurable"]['km_route_llm_model'],
                         base_url=config["configurable"]['km_route_llm_api_base'],
                         api_key=config["configurable"]['km_route_llm_api_key'],
                         temperature=0.01)

        # 使用模板生成知识路由选择prompt
        template_data = {
            'km_info': km_info,
            'user_message': config["configurable"]["graph_request"].user_message
        }
        selected_knowledge_prompt = TemplateLoader.render_template(
            'prompts/graph/knowledge_route_selection_prompt',
            template_data
        )

        logger.debug(f"知识路由选择Prompt: {selected_knowledge_prompt}")
        selected_km_response = llm.invoke(selected_knowledge_prompt)
        return json_repair.loads(selected_km_response.content)

    async def _execute_graph_rag(self, rag_search_request) -> list:
        """执行图谱RAG检索并处理结果"""
        try:
            # 执行图谱检索
            graph_result = await self._perform_graph_search(rag_search_request)
            if not graph_result:
                logger.warning("GraphRAG检索结果为空")
                return []

            # 处理检索结果
            return self._process_graph_results(graph_result, rag_search_request.graph_rag_request.group_ids)

        except Exception as e:
            logger.error(f"GraphRAG检索处理异常: {str(e)}")
            return []

    async def _perform_graph_search(self, rag_search_request) -> list:
        """执行图谱搜索"""
        graphiti = GraphitiRAG()
        rag_search_request.graph_rag_request.search_query = rag_search_request.search_query
        graph_result = await graphiti.search(req=rag_search_request.graph_rag_request)

        logger.info(
            f"GraphRAG模式检索知识库: {rag_search_request.graph_rag_request.group_ids}, "
            f"结果数量: {len(graph_result)}"
        )
        return graph_result

    def _process_graph_results(self, graph_result: list, group_ids: list) -> list:
        """处理图谱检索结果"""
        seen_relations = set()
        summary_dict = {}  # 用于去重summary
        processed_results = []

        # 使用默认的group_id，避免在循环中重复获取
        default_group_id = group_ids[0] if group_ids else ''

        for graph_item in graph_result:
            # 处理关系事实
            relation_result = self._process_relation_fact(
                graph_item, seen_relations, default_group_id
            )
            if relation_result:
                processed_results.append(relation_result)

            # 收集summary信息
            self._collect_summary_info(graph_item, summary_dict)

        # 生成去重的summary结果
        summary_results = self._generate_summary_results(
            summary_dict, default_group_id)
        processed_results.extend(summary_results)

        return processed_results

    def _process_relation_fact(self, graph_item: dict, seen_relations: set, group_id: str):
        """处理单个关系事实"""
        source_node = graph_item.get('source_node', {})
        target_node = graph_item.get('target_node', {})
        source_name = source_node.get('name', '')
        target_name = target_node.get('name', '')
        fact = graph_item.get('fact', '')

        if not (fact and source_name and target_name):
            return None

        relation_content = f"关系事实: {source_name} - {fact} - {target_name}"
        if relation_content in seen_relations:
            return None

        seen_relations.add(relation_content)
        return self._create_relation_result_object(
            relation_content, source_name, target_name, group_id
        )

    def _collect_summary_info(self, graph_item: dict, summary_dict: dict):
        """收集并去重summary信息"""
        source_node = graph_item.get('source_node', {})
        target_node = graph_item.get('target_node', {})

        for node_data in [source_node, target_node]:
            node_name = node_data.get('name', '')
            node_summary = node_data.get('summary', '')

            if node_name and node_summary:
                if node_summary not in summary_dict:
                    summary_dict[node_summary] = set()
                summary_dict[node_summary].add(node_name)

    def _generate_summary_results(self, summary_dict: dict, group_id: str) -> list:
        """生成去重的summary结果"""
        summary_results = []
        for summary_content, associated_nodes in summary_dict.items():
            nodes_list = ', '.join(sorted(associated_nodes))
            summary_with_nodes = f"节点详情: 以下内容与节点 [{nodes_list}] 相关:\n{summary_content}"

            summary_result = self._create_summary_result_object(
                summary_with_nodes, nodes_list, group_id, summary_content
            )
            summary_results.append(summary_result)

        return summary_results

    def _create_relation_result_object(self, relation_content: str, source_name: str,
                                       target_name: str, group_id: str):
        """创建关系事实结果对象"""
        content_hash = hash(relation_content) % 100000

        class RelationResult:
            def __init__(self):
                self.page_content = relation_content
                self.metadata = {
                    'knowledge_title': f"图谱关系: {source_name} - {target_name}",
                    'knowledge_id': group_id,
                    'chunk_number': 1,
                    'chunk_id': f"relation_{content_hash}",
                    'segment_number': 1,
                    'segment_id': f"relation_{content_hash}",
                    'chunk_type': 'Graph'
                }

        return RelationResult()

    def _create_summary_result_object(self, summary_with_nodes: str, nodes_list: str,
                                      group_id: str, summary_content: str):
        """创建summary结果对象"""
        content_hash = hash(summary_content) % 100000

        class SummaryResult:
            def __init__(self):
                self.page_content = summary_with_nodes
                self.metadata = {
                    'knowledge_title': f"图谱节点详情: {nodes_list}",
                    'knowledge_id': group_id,
                    'chunk_number': 1,
                    'chunk_id': f"summary_{content_hash}",
                    'segment_number': 1,
                    'segment_id': f"summary_{content_hash}",
                    'chunk_type': 'Document'
                }

        return SummaryResult()

        return SummaryResult()

    def _prepare_template_data(self, rag_result: list, config: RunnableConfig) -> dict:
        """准备模板渲染所需的数据"""
        # 转换RAG结果为模板友好的格式
        rag_results = []
        for r in rag_result:
            # 直接从metadata获取数据（PgvectorRag返回扁平结构）
            metadata = getattr(r, 'metadata', {})
            rag_results.append({
                'title': metadata.get('knowledge_title', 'N/A'),
                'knowledge_id': metadata.get('knowledge_id', 0),
                'chunk_number': metadata.get('chunk_number', 0),
                'chunk_id': metadata.get('chunk_id', 'N/A'),
                'segment_number': metadata.get('segment_number', 0),
                'segment_id': metadata.get('segment_id', 'N/A'),
                'content': r.page_content,
                'chunk_type': metadata.get('chunk_type', 'Document')
            })

        # 准备模板数据
        template_data = {
            'rag_results': rag_results,
            'enable_rag_source': config["configurable"].get("enable_rag_source", False),
            'enable_rag_strict_mode': config["configurable"].get("enable_rag_strict_mode", False)
        }

        return template_data

    def _process_document_content(self, doc):
        """
        根据 is_doc 字段处理文档内容

        Args:
            doc: 文档对象，包含 page_content 和 metadata

        Returns:
            处理后的文档对象
        """
        # 获取元数据
        metadata = getattr(doc, 'metadata', {})
        is_doc = metadata.get('is_doc')

        logger.debug(f"处理文档内容 - is_doc: {is_doc}")

        if is_doc == "0":
            # QA类型：用 qa_question 和 qa_answer 组合替换 page_content
            qa_question = metadata.get('qa_question')
            qa_answer = metadata.get('qa_answer')

            if qa_question and qa_answer:
                doc.page_content = f"问题: {qa_question}\n答案: {qa_answer}"
                doc.metadata['knowledge_title'] = qa_question
            doc.metadata['chunk_type'] = 'QA'
        elif is_doc == "1":
            # 文档类型：直接 append qa_answer
            qa_answer = metadata.get('qa_answer')
            if qa_answer:
                doc.page_content += f"\n{qa_answer}"
            doc.metadata['chunk_type'] = 'Document'
        else:
            # 默认为文档类型
            doc.metadata['chunk_type'] = 'Document'

        return doc

    def user_message_node(self, state: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
        state["messages"].append(HumanMessage(
            content=config["configurable"]["graph_request"].user_message))
        return state
