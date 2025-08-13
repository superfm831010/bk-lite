"""
模板加载器模块
用于加载和渲染 Jinja2 模板
"""
import os
from pathlib import Path
from typing import Dict, Any, Optional, Union

from jinja2 import Environment, FileSystemLoader, Template, TemplateNotFound
from sanic.log import logger


class TemplateLoader:
    """
    Jinja2 模板加载器

    用于加载 templates/{module}/{file} 路径下的模板文件并渲染
    """

    def __init__(self, base_path: Optional[str] = None):
        """
        初始化模板加载器

        Args:
            base_path: 模板文件的基础路径，默认为当前工作目录下的 templates 文件夹
        """
        if base_path is None:
            base_path = os.path.join(os.getcwd(), "templates")

        self.base_path = Path(base_path)

        # 确保模板目录存在
        if not self.base_path.exists():
            logger.warning(f"Templates directory does not exist: {self.base_path}")
            self.base_path.mkdir(parents=True, exist_ok=True)

        # 初始化 Jinja2 环境
        self.env = Environment(
            loader=FileSystemLoader(str(self.base_path)),
            autoescape=True,  # 默认开启自动转义
            trim_blocks=True,
            lstrip_blocks=True
        )

        logger.info(f"TemplateLoader initialized with base_path: {self.base_path}")

    def load_template(self, module: str, filename: str, context: Optional[Dict[str, Any]] = None) -> Union[Template, str]:
        """
        加载指定模块和文件名的模板

        Args:
            module: 模块名称
            filename: 模板文件名
            context: 可选的模板渲染上下文变量，如果提供则直接返回渲染后的文本

        Returns:
            如果提供了 context，返回渲染后的文本内容；否则返回 Jinja2 Template 对象

        Raises:
            TemplateNotFound: 当模板文件不存在时
        """
        template_path = f"{module}/{filename}"

        try:
            template = self.env.get_template(template_path)
            logger.debug(f"Template loaded successfully: {template_path}")

            # 如果提供了 context，直接渲染并返回文本
            if context is not None:
                rendered_text = template.render(**context)
                logger.debug(f"Template rendered with context: {template_path}, context_keys: {list(context.keys())}")
                return rendered_text

            return template
        except TemplateNotFound as e:
            logger.error(f"Template not found: {template_path}, base_path: {self.base_path}")
            raise e

    def render_template(self, module: str, filename: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        渲染指定模块和文件名的模板

        Args:
            module: 模块名称
            filename: 模板文件名
            context: 模板渲染上下文变量，默认为空字典

        Returns:
            渲染后的文本内容

        Raises:
            TemplateNotFound: 当模板文件不存在时
        """
        if context is None:
            context = {}

        template_path = f"{module}/{filename}"

        try:
            template = self.load_template(module, filename)
            rendered_text = template.render(**context)

            logger.debug(f"Template rendered successfully: {template_path}, context_keys: {list(context.keys())}")
            return rendered_text

        except Exception as e:
            logger.error(f"Failed to render template: {template_path}, error: {str(e)}")
            raise e

    def template_exists(self, module: str, filename: str) -> bool:
        """
        检查指定模板是否存在

        Args:
            module: 模块名称
            filename: 模板文件名

        Returns:
            True 如果模板存在，否则 False
        """
        template_path = self.base_path / module / filename
        exists = template_path.exists() and template_path.is_file()

        logger.debug(f"Template exists check: {module}/{filename} -> {exists}")
        return exists

    def list_templates(self, module: str) -> list[str]:
        """
        列出指定模块下的所有模板文件

        Args:
            module: 模块名称

        Returns:
            模板文件名列表
        """
        module_path = self.base_path / module

        if not module_path.exists():
            logger.warning(f"Module directory does not exist: {module_path}")
            return []

        templates = []
        for file_path in module_path.iterdir():
            if file_path.is_file() and file_path.suffix in ['.html', '.txt', '.j2', '.jinja2']:
                templates.append(file_path.name)

        logger.debug(f"Found {len(templates)} templates in module: {module}")
        return templates
