import base64
import logging
import hashlib
from typing import Dict, Optional, Any

from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings

logger = logging.getLogger(__name__)


class EncryptMixin:
    # 常量定义，避免魔法数字
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
            # 使用SHA256确保密钥长度和安全性
            secret_key = settings.SECRET_KEY.encode(EncryptMixin.ENCODING)
            key_hash = hashlib.sha256(secret_key).digest()
            key = base64.urlsafe_b64encode(key_hash)
            
            cipher_suite = Fernet(key)
            logger.debug("Cipher suite created successfully")
            return cipher_suite
            
        except Exception as e:
            logger.error(f"Failed to create cipher suite: {e}")
            raise ValueError(f"Invalid SECRET_KEY configuration: {e}")

    @classmethod
    def encrypt_field(cls, field_name: str, field_dict: Optional[Dict[str, Any]] = None) -> None:
        """
        加密字典中指定字段的值
        
        Args:
            field_name: 要加密的字段名
            field_dict: 包含字段的字典，如果为None则使用空字典
        """
        if field_dict is None:
            field_dict = {}
            logger.warning(f"encrypt_field called with None field_dict for field '{field_name}'")
            return
            
        if field_name not in field_dict:
            logger.info(f"Field '{field_name}' not found in field_dict, skipping encryption")
            return
            
        field_value = field_dict[field_name]
        
        # 跳过空值和None值
        if not field_value:
            logger.debug(f"Field '{field_name}' is empty or None, skipping encryption")
            return
            
        if not isinstance(field_value, str):
            logger.warning(f"Field '{field_name}' value is not string type: {type(field_value)}, skipping encryption")
            return
            
        try:
            cipher_suite = cls.get_cipher_suite()
            
            # 检查是否已经加密
            try:
                cipher_suite.decrypt(field_value.encode(cls.ENCODING))
                logger.debug(f"Field '{field_name}' is already encrypted, skipping")
                return
            except InvalidToken:
                # 值未加密，继续加密流程
                pass
            except Exception as e:
                logger.warning(f"Unexpected error during encryption check for field '{field_name}': {e}")
                return
                
            # 执行加密
            encrypted_value = cipher_suite.encrypt(field_value.encode(cls.ENCODING))
            field_dict[field_name] = encrypted_value.decode(cls.ENCODING)
            logger.info(f"Field '{field_name}' encrypted successfully")
            
        except ValueError as e:
            logger.error(f"Cipher suite creation failed during encryption of field '{field_name}': {e}")
        except Exception as e:
            logger.error(f"Unexpected error during encryption of field '{field_name}': {e}")

    @classmethod
    def decrypt_field(cls, field_name: str, field_dict: Optional[Dict[str, Any]] = None) -> None:
        """
        解密字典中指定字段的值
        
        Args:
            field_name: 要解密的字段名
            field_dict: 包含字段的字典，如果为None则使用空字典
        """
        if field_dict is None:
            field_dict = {}
            logger.warning(f"decrypt_field called with None field_dict for field '{field_name}'")
            return
            
        if field_name not in field_dict:
            logger.info(f"Field '{field_name}' not found in field_dict, skipping decryption")
            return
            
        field_value = field_dict[field_name]
        
        # 跳过空值和None值
        if not field_value:
            logger.debug(f"Field '{field_name}' is empty or None, skipping decryption")
            return
            
        if not isinstance(field_value, str):
            logger.warning(f"Field '{field_name}' value is not string type: {type(field_value)}, skipping decryption")
            return
            
        try:
            cipher_suite = cls.get_cipher_suite()
            decrypted_value = cipher_suite.decrypt(field_value.encode(cls.ENCODING))
            field_dict[field_name] = decrypted_value.decode(cls.ENCODING)
            logger.info(f"Field '{field_name}' decrypted successfully")
            
        except InvalidToken:
            logger.debug(f"Field '{field_name}' appears to be plain text, no decryption needed")
        except ValueError as e:
            logger.error(f"Cipher suite creation failed during decryption of field '{field_name}': {e}")
        except Exception as e:
            logger.error(f"Unexpected error during decryption of field '{field_name}': {e}")
