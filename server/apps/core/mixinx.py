import base64
import logging
import hashlib
from typing import Dict, Optional, Any

from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings

logger = logging.getLogger(__name__)


class EncryptMixin:
    # 常量定义
    KEY_LENGTH = 32
    ENCODING = 'utf-8'
    
    @staticmethod
    def get_cipher_suite() -> Fernet:
        """
        创建加密套件实例
        
        Returns:
            Fernet: 加密套件实例
            
        Raises:
            ValueError: 当SECRET_KEY配置无效时
        """
        try:
            secret_key = settings.SECRET_KEY.encode(EncryptMixin.ENCODING)
            key_hash = hashlib.sha256(secret_key).digest()
            key = base64.urlsafe_b64encode(key_hash)
            return Fernet(key)
        except Exception as e:
            logger.error(f"Failed to create cipher suite: {e}")
            raise ValueError(f"Invalid SECRET_KEY configuration: {e}")

    @classmethod
    def encrypt_field(cls, field_name: str, field_dict: Optional[Dict[str, Any]] = None) -> None:
        """
        加密字典中指定字段的值
        
        Args:
            field_name: 要加密的字段名
            field_dict: 包含字段的字典
        """
        if not field_dict or field_name not in field_dict:
            return
            
        field_value = field_dict[field_name]
        if not field_value or not isinstance(field_value, str):
            return
            
        try:
            cipher_suite = cls.get_cipher_suite()
            encrypted_value = cipher_suite.encrypt(field_value.encode(cls.ENCODING))
            field_dict[field_name] = encrypted_value.decode(cls.ENCODING)
        except Exception as e:
            logger.error(f"Failed to encrypt field '{field_name}': {e}")

    @classmethod
    def decrypt_field(cls, field_name: str, field_dict: Optional[Dict[str, Any]] = None) -> None:
        """
        解密字典中指定字段的值
        
        Args:
            field_name: 要解密的字段名
            field_dict: 包含字段的字典
        """
        if not field_dict or field_name not in field_dict:
            return
            
        field_value = field_dict[field_name]
        if not field_value or not isinstance(field_value, str):
            return
            
        try:
            cipher_suite = cls.get_cipher_suite()
            decrypted_value = cipher_suite.decrypt(field_value.encode(cls.ENCODING))
            field_dict[field_name] = decrypted_value.decode(cls.ENCODING)
        except InvalidToken:
            # 字段可能是明文，跳过解密
            pass
        except Exception as e:
            logger.error(f"Failed to decrypt field '{field_name}': {e}")
