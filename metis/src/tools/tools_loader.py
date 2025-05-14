from src.core.entity.tools_server import ToolsServer
from src.tools.jenkins_tools import list_jenkins_jobs, trigger_jenkins_build
from src.tools.python_tools import python_analyze_repl
from src.tools.search_tools import duckduckgo_search
from src.tools.time_tools import get_current_time
from src.tools.kubernetes_tools import (
    get_kubernetes_namespaces, list_kubernetes_pods, list_kubernetes_nodes,
    list_kubernetes_deployments, list_kubernetes_services, list_kubernetes_events,
    get_failed_kubernetes_pods, get_pending_kubernetes_pods, get_high_restart_kubernetes_pods,
    get_kubernetes_node_capacity, get_kubernetes_orphaned_resources,
    get_kubernetes_resource_yaml, get_kubernetes_pod_logs
)
from src.tools.ansible_tools import ansible_adhoc
from src.tools.http_request_tools import (
    http_get, http_post, http_put, http_delete)

import copy

ToolsMap = {
    'current_time': [
        {
            "func": get_current_time,
            'enable_extra_prompt': False,
        }
    ],
    'duckduckgo': [
        {
            "func": duckduckgo_search,
            'enable_extra_prompt': False,
        }
    ],
    'jenkins': [
        {
            "func": list_jenkins_jobs,
            'enable_extra_prompt': False,
        },
        {
            "func": trigger_jenkins_build,
            'enable_extra_prompt': False,
        }
    ],
    'python_analyze_repl': [
        {
            "func": python_analyze_repl,
            'enable_extra_prompt': False,
        }
    ],
    'kubernetes': [
        {
            "func": get_kubernetes_namespaces,
            'enable_extra_prompt': False,
        },
        {
            "func": list_kubernetes_pods,
            'enable_extra_prompt': False,
        },
        {
            "func": list_kubernetes_nodes,
            'enable_extra_prompt': False,
        },
        {
            "func": list_kubernetes_deployments,
            'enable_extra_prompt': False,
        },
        {
            "func": list_kubernetes_services,
            'enable_extra_prompt': False,
        },
        {
            "func": list_kubernetes_events,
            'enable_extra_prompt': False,
        },
        {
            "func": get_failed_kubernetes_pods,
            'enable_extra_prompt': False,
        },
        {
            "func": get_pending_kubernetes_pods,
            'enable_extra_prompt': False,
        },
        {
            "func": get_high_restart_kubernetes_pods,
            'enable_extra_prompt': False,
        },
        {
            "func": get_kubernetes_node_capacity,
            'enable_extra_prompt': False,
        },
        {
            "func": get_kubernetes_orphaned_resources,
            'enable_extra_prompt': False,
        },
        {
            "func": get_kubernetes_resource_yaml,
            'enable_extra_prompt': False,
        },
        {
            "func": get_kubernetes_pod_logs,
            'enable_extra_prompt': False,
        }
    ],
    "ansible": [
        {
            "func": ansible_adhoc,
            'enable_extra_prompt': False,
        }
    ],
    "http_request": [
        {
            "func": http_get,
            'enable_extra_prompt': True,
        },
        {
            "func": http_post,
            'enable_extra_prompt': True,
        },
        {
            "func": http_put,
            'enable_extra_prompt': True,
        },
        {
            "func": http_delete,
            'enable_extra_prompt': True,
        }
    ]

}


class ToolsLoader:

    @staticmethod
    def load_tools(tool_server: ToolsServer):
        tools = []
        tools_name = tool_server.url.split(":")[1]
        for tool in ToolsMap[tools_name]:
            cp_tool = copy.deepcopy(tool)
            func = cp_tool['func']
            enable_extra_prompt = cp_tool['enable_extra_prompt']
            if enable_extra_prompt:
                final_prompt = f"""以下是函数的动态参数生成要求，param json 参数说明:\n"""
                for key, value in tool_server.extra_prompt.items():
                    final_prompt += f"{key}:{value}，"
                final_prompt += f"""
                    请根据以上要求生成函数的动态参数, param为json字典字符串
                """
                func.description += final_prompt
                tools.append(func)
            else:
                tools.append(func)
        return tools
