import hashlib
import logging
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import urlsafe_b64decode, urlsafe_b64encode
from config.components.base import SECRET_KEY

logger = logging.getLogger(__name__)


class AESCryptor:
    PADDING_CHAR = "="
    PADDING_BLOCK_SIZE = 4

    def __init__(self):
        if not SECRET_KEY:
            raise ValueError("SECRET_KEY 不能为空")

        self.__encryptKey = SECRET_KEY
        self.__key = hashlib.md5(self.__encryptKey.encode("utf8")).digest()
        self.__block_size = AES.block_size
        logger.info("AESCryptor 初始化完成")

    def encode(self, plaintext):
        """ AES encryption """
        if not plaintext:
            raise ValueError("待加密文本不能为空")

        try:
            logger.debug("开始 AES 编码")
            iv = AES.new(self.__key, AES.MODE_CBC).iv
            cipher = AES.new(self.__key, AES.MODE_CBC, iv)
            ciphertext = cipher.encrypt(pad(plaintext.encode("utf8"), self.__block_size))
            result = urlsafe_b64encode(iv + ciphertext).decode("utf8").rstrip(self.PADDING_CHAR)
            logger.debug("AES 编码完成")
            return result
        except Exception as e:
            logger.error(f"AES 编码失败: {e}")
            raise

    def decode(self, ciphertext):
        """ AES decryption """
        if not ciphertext:
            raise ValueError("待解密文本不能为空")

        try:
            logger.debug("开始 AES 解码")
            # 补齐 base64 填充
            padding_needed = self.PADDING_BLOCK_SIZE - len(ciphertext) % self.PADDING_BLOCK_SIZE
            padded_ciphertext = ciphertext + self.PADDING_CHAR * padding_needed

            decoded_data = urlsafe_b64decode(padded_ciphertext)

            if len(decoded_data) < self.__block_size:
                raise ValueError("加密数据格式错误：长度不足")

            iv = decoded_data[:self.__block_size]
            actual_ciphertext = decoded_data[self.__block_size:]
            cipher = AES.new(self.__key, AES.MODE_CBC, iv)
            result = unpad(cipher.decrypt(actual_ciphertext), self.__block_size).decode("utf8")
            logger.debug("AES 解码完成")
            return result
        except Exception as e:
            logger.error(f"AES 解码失败: {e}")
            raise
