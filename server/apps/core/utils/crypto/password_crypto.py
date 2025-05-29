import base64
import hashlib
import logging

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

logger = logging.getLogger(__name__)


class PasswordCrypto:
    def __init__(self, key: str):
        if not key:
            raise ValueError("密钥不能为空")
        
        # 使用SHA256确保密钥长度和强度
        self.key = hashlib.sha256(key.encode("utf-8")).digest()[:32]
        self.mode = AES.MODE_CBC

    def encrypt(self, plaintext: str) -> str:
        if not plaintext:
            raise ValueError("待加密文本不能为空")

        try:
            cipher = AES.new(self.key, self.mode)
            iv = cipher.iv
            ciphertext = cipher.encrypt(pad(plaintext.encode("utf-8"), AES.block_size))
            return base64.b64encode(iv + ciphertext).decode("utf-8")
        except Exception as e:
            logger.error(f"AES 加密失败: {e}")
            raise

    def decrypt(self, encrypted_text: str) -> str:
        if not encrypted_text:
            raise ValueError("待解密文本不能为空")

        try:
            data = base64.b64decode(encrypted_text)

            if len(data) < AES.block_size:
                raise ValueError("加密数据格式错误：长度不足")

            iv = data[:AES.block_size]
            ciphertext = data[AES.block_size:]
            cipher = AES.new(self.key, self.mode, iv)
            plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
            return plaintext.decode("utf-8")
        except Exception as e:
            logger.error(f"AES 解密失败: {e}")
            raise
