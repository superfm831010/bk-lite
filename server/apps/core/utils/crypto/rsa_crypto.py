import base64
import logging
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

logger = logging.getLogger(__name__)


class RSACryptor:
    DEFAULT_KEY_SIZE = 2048
    MIN_KEY_SIZE = 1024

    def __init__(self, bits=DEFAULT_KEY_SIZE):
        if bits < self.MIN_KEY_SIZE:
            raise ValueError(f"密钥长度不能小于 {self.MIN_KEY_SIZE} 位")

        try:
            logger.info(f"生成 RSA 密钥对，长度: {bits} 位")
            self.key = RSA.generate(bits)
            self.private_key = self.key.export_key()
            self.public_key = self.key.publickey().export_key()
            logger.info("RSA 密钥对生成成功")
        except Exception as e:
            logger.error(f"RSA 密钥生成失败: {e}")
            raise

    def encrypt_rsa(self, plain_text, public_key):
        if not plain_text:
            raise ValueError("待加密文本不能为空")
        if not public_key:
            raise ValueError("公钥不能为空")

        try:
            logger.debug("开始 RSA 加密")
            rsakey = RSA.import_key(public_key)
            cipher = PKCS1_OAEP.new(rsakey)
            encrypted_text = cipher.encrypt(plain_text.encode("utf-8"))
            result = base64.b64encode(encrypted_text).decode("utf-8")
            logger.debug("RSA 加密完成")
            return result
        except Exception as e:
            logger.error(f"RSA 加密失败: {e}")
            raise

    def decrypt_rsa(self, encrypted_text, private_key):
        if not encrypted_text:
            raise ValueError("待解密文本不能为空")
        if not private_key:
            raise ValueError("私钥不能为空")

        try:
            logger.debug("开始 RSA 解密")
            rsakey = RSA.import_key(private_key)
            cipher = PKCS1_OAEP.new(rsakey)
            decoded_data = base64.b64decode(encrypted_text.encode("utf-8"))
            decrypted_text = cipher.decrypt(decoded_data).decode("utf-8")
            logger.debug("RSA 解密完成")
            return decrypted_text
        except Exception as e:
            logger.error(f"RSA 解密失败: {e}")
            raise
