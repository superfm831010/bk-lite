from pydantic import BaseModel


class ToolsServer(BaseModel):
    name: str
    url: str
    command: str = ''
    args: list = []
    extra_param_prompt: dict = {}
    extra_tools_prompt: str = ''
