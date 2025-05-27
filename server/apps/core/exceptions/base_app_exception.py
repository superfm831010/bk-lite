import logging
from typing import Any, Dict, Optional, Union


class BaseAppException(Exception):
    ERROR_CODE = "0000000"
    MESSAGE = "APP异常"
    STATUS_CODE = 500
    LOG_LEVEL = logging.ERROR

    def __init__(self, message: Optional[str] = None, data: Any = None, *args):
        """
        初始化应用异常

        :param message: 错误消息，如果为None则使用类的默认MESSAGE
        :param data: 附加数据，可以是任意类型
        :param args: 传递给父类Exception的其他参数
        """
        super(BaseAppException, self).__init__(*args)

        # 参数验证和处理
        if message is not None and not isinstance(message, str):
            # 如果message不是字符串，转换为字符串并记录警告
            message = str(message)
            logging.warning(
                "BaseAppException message参数应该是字符串类型，已自动转换。原类型: %s",
                type(message).__name__,
            )

        self.message = self.MESSAGE if message is None else message
        self.data = data

        # 记录异常创建日志，便于运维排查
        logger = logging.getLogger(self.__class__.__module__)
        logger.log(
            self.LOG_LEVEL,
            "异常创建 - 类型: %s, 错误码: %s, 消息: %s, 数据类型: %s",
            self.__class__.__name__,
            self.ERROR_CODE,
            self.message,
            type(self.data).__name__ if self.data is not None else "None",
        )

    def render_data(self) -> Any:
        """
        渲染异常数据

        :return: 处理后的数据，默认直接返回原始数据
        """
        return self.data

    def response_data(self) -> Dict[str, Union[bool, str, Any]]:
        """
        生成标准的响应数据格式

        :return: 包含result、code、message、data的字典
        """
        response = {
            "result": False,
            "code": self.ERROR_CODE,
            "message": self.message,
            "data": self.render_data(),
        }

        # 记录响应数据生成日志
        logger = logging.getLogger(self.__class__.__module__)
        logger.debug(
            "异常响应数据生成 - 错误码: %s, 消息长度: %d",
            self.ERROR_CODE,
            len(self.message) if self.message else 0,
        )

        return response
