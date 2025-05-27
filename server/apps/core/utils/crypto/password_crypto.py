import base64
import logging

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

logger = logging.getLogger(__name__)


class PasswordCrypto:
    VALID_KEY_SIZES = (16, 24, 32)
    DEFAULT_KEY_SIZE = 32

    def __init__(self, key: str):
        if not key:
            raise ValueError("密钥不能为空")
        if len(key) < 8:
            logger.warning("密钥长度过短，建议使用更强的密钥")

        # 确保密钥长度为 16, 24 或 32 字节
        self.key = key.encode("utf-8").ljust(self.DEFAULT_KEY_SIZE)[: self.DEFAULT_KEY_SIZE]
        self.mode = AES.MODE_CBC
        logger.info("PasswordCrypto 初始化完成")

    def encrypt(self, plaintext: str) -> str:
        if not plaintext:
            raise ValueError("待加密文本不能为空")

        try:
            logger.debug("开始 AES 加密")
            cipher = AES.new(self.key, self.mode)
            iv = cipher.iv  # 初始化向量
            ciphertext = cipher.encrypt(pad(plaintext.encode("utf-8"), AES.block_size))
            # 返回 base64 编码的 iv 和密文
            result = base64.b64encode(iv + ciphertext).decode("utf-8")
            logger.debug("AES 加密完成")
            return result
        except Exception as e:
            logger.error(f"AES 加密失败: {e}")
            raise

    def decrypt(self, encrypted_text: str) -> str:
        if not encrypted_text:
            raise ValueError("待解密文本不能为空")

        try:
            logger.debug("开始 AES 解密")
            data = base64.b64decode(encrypted_text)

            if len(data) < AES.block_size:
                raise ValueError("加密数据格式错误：长度不足")

            iv = data[: AES.block_size]  # 提取 iv
            ciphertext = data[AES.block_size :]
            cipher = AES.new(self.key, self.mode, iv)
            plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
            result = plaintext.decode("utf-8")
            logger.debug("AES 解密完成")
            return result
        except Exception as e:
            logger.error(f"AES 解密失败: {e}")
            raise
