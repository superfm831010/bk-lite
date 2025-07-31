from typing import Any, Dict, List

import docker
from django.conf import settings

from apps.core.logger import opspilot_logger as logger


class LobeDockerClient(object):
    def __init__(self):
        """
        初始化Docker客户端
        Docker socket默认挂载到容器中，使用默认的客户端配置
        """
        try:
            self.client = docker.from_env()
            self.api_client = docker.APIClient()
            logger.info("Docker客户端初始化成功")
        except Exception as e:
            logger.error(f"Docker客户端初始化失败: {e}")
            raise Exception("无法连接到Docker服务，请检查Docker是否正常运行。")

    def start_pilot(self, bot) -> bool:
        """
        启动LobeChat容器
        :param bot: Bot模型实例
        :return: 是否成功启动
        """
        container_name = f"lobe_chat-{bot.id}"
        skill_list = [f"+{i.name}" for i in bot.llm_skills.all()]

        # 构建环境变量
        environment = {
            "TZ": "Asia/Shanghai",
            "OPENAI_API_KEY": bot.api_token,  # 使用bot的api_token作为OpenAI API Key
            "OPENAI_PROXY_URL": settings.MUNCHKIN_BASE_URL.strip("/") + "/opspilot/bot_mgmt/lobe_chat/v1/",  # 代理URL配置
            "BK_LITE_APP_ID": bot.id,
            "OPENAI_MODEL_LIST": ",".join(skill_list),
        }

        # 端口映射配置 - 修改为3000端口
        ports = {"3000/tcp": None}  # 默认随机分配主机端口
        if bot.enable_node_port and bot.node_port:
            ports["3000/tcp"] = bot.node_port

        # 配置标签
        labels = {"app": "lobe_chat", "bot-id": str(bot.id)}

        # 如果存在bot_domain，添加Traefik相关标签
        if bot.bot_domain:
            labels.update(
                {
                    "traefik.enable": "true",
                    f"traefik.http.routers.lobe_chat-{bot.id}.rule": f"Host(`{bot.bot_domain}`)",
                    f"traefik.http.routers.lobe_chat-{bot.id}.entrypoints": "https",
                    f"traefik.http.routers.lobe_chat-{bot.id}.tls": "true",
                    f"traefik.http.services.lobe_chat-{bot.id}.loadbalancer.server.port": "3000",
                }
            )

        try:
            # 验证必要的配置参数
            if not bot.api_token:
                raise ValueError("Bot API token 不能为空")

            # 检查是否已存在同名容器，如存在则先移除
            self._remove_container_if_exists(container_name)

            # 创建并启动容器 - 移除复杂的command，使用默认启动
            container = self.client.containers.run(
                image="bklite/lobe-chat:latest",
                name=container_name,
                detach=True,
                environment=environment,
                ports=ports,
                labels=labels,
                restart_policy={"Name": "always"},
                network=settings.CONVERSATION_DOCKER_NETWORK,
                # 移除command参数，使用镜像默认启动命令
            )
            logger.info(f"启动Pilot[{bot.id}]容器成功，容器ID: {container.id}")
            return True
        except Exception as e:
            logger.error(f"启动LobeChat[{bot.id}]容器失败: {e}")
            return False

    def stop_pilot(self, bot_id) -> bool:
        """
        停止并移除LobeChat容器
        :param bot_id: Bot ID
        :return: 是否成功停止
        """
        container_name = f"lobe_chat-{bot_id}"
        try:
            return self._remove_container_if_exists(container_name)
        except Exception as e:
            logger.error(f"停止LobeChat[{bot_id}]容器失败: {e}")
            return False

    def list_pilot(self) -> List[Dict[str, Any]]:
        """
        列出所有LobeChat容器
        :return: 容器列表
        """
        try:
            containers = self.client.containers.list(all=True, filters={"label": "app=lobe_chat"})
            container_list = [
                {"name": container.name, "status": container.status, "id": container.id[:12]}
                for container in containers
            ]
            logger.info(f"共找到 {len(container_list)} 个LobeChat容器")
            return container_list
        except Exception as e:
            logger.error(f"列出LobeChat容器失败: {e}")
            return []

    def _remove_container_if_exists(self, container_name) -> bool:
        """
        如果容器存在则停止并删除
        :param container_name: 容器名称
        :return: 是否成功操作
        """
        try:
            try:
                container = self.client.containers.get(container_name)
                if container.status == "running":
                    container.stop(timeout=10)
                    logger.info(f"停止容器 {container_name} 成功")
                container.remove(force=True)
                logger.info(f"删除容器 {container_name} 成功")
                return True
            except docker.errors.NotFound:
                # 容器不存在，不需要操作
                return True
        except Exception as e:
            logger.error(f"移除容器 {container_name} 失败: {e}")
            return False
