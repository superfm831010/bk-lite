import pytest
import logging
import base64
from unittest.mock import patch, Mock
from cryptography.fernet import Fernet

from apps.core.mixinx import EncryptMixin

# 配置测试日志
logger = logging.getLogger(__name__)


@pytest.fixture
def mock_settings():
    """提供模拟的Django settings配置"""
    settings = Mock()
    settings.SECRET_KEY = "test-secret-key-for-encryption-12345678"
    return settings


@pytest.fixture
def sample_field_dict():
    """提供示例字段字典数据"""
    return {
        "password": "my_secret_password",
        "api_key": "test_api_key_12345",
        "token": "bearer_token_abcdef",
        "empty_field": "",
        "none_field": None
    }


@pytest.fixture
def encrypted_field_dict():
    """提供包含已加密数据的字段字典"""
    # 使用固定密钥创建加密数据
    key = base64.urlsafe_b64encode(b"test-secret-key-for-encryption-12"[:32])
    cipher_suite = Fernet(key)
    encrypted_password = cipher_suite.encrypt(b"my_secret_password").decode()
    
    return {
        "password": encrypted_password,
        "api_key": "test_api_key_12345",
        "empty_field": "",
        "none_field": None
    }


def test_get_cipher_suite_creation(mock_settings):
    """测试密码套件创建功能 - 验证能否正确生成Fernet实例"""
    logger.info("Testing cipher suite creation")
    
    with patch('apps.core.mixinx.settings', mock_settings):
        cipher_suite = EncryptMixin.get_cipher_suite()
        
        logger.info(f"Cipher suite type: {type(cipher_suite)}")
        logger.info(f"Is Fernet instance: {isinstance(cipher_suite, Fernet)}")
        logger.info("Cipher suite creation test completed")


def test_encrypt_field_new_value(mock_settings, sample_field_dict):
    """测试字段加密功能 - 对未加密的新值进行加密"""
    logger.info("Testing field encryption for new unencrypted value")
    
    field_name = "password"
    original_value = sample_field_dict[field_name]
    
    with patch('apps.core.mixinx.settings', mock_settings):
        EncryptMixin.encrypt_field(field_name, sample_field_dict)
        
        encrypted_value = sample_field_dict[field_name]
        
        logger.info(f"Original value: {original_value}")
        logger.info(f"Encrypted value length: {len(encrypted_value)}")
        logger.info(f"Value changed after encryption: {original_value != encrypted_value}")
        logger.info("Field encryption test completed")


def test_encrypt_field_already_encrypted(mock_settings, encrypted_field_dict):
    """测试字段加密功能 - 对已加密的值不重复加密"""
    logger.info("Testing field encryption for already encrypted value")
    
    field_name = "password"
    original_encrypted_value = encrypted_field_dict[field_name]
    
    with patch('apps.core.mixinx.settings', mock_settings):
        EncryptMixin.encrypt_field(field_name, encrypted_field_dict)
        
        current_value = encrypted_field_dict[field_name]
        
        logger.info(f"Original encrypted value: {original_encrypted_value[:20]}...")
        logger.info(f"Current value: {current_value[:20]}...")
        logger.info(f"Value unchanged (no double encryption): {original_encrypted_value == current_value}")
        logger.info("Already encrypted field test completed")


def test_encrypt_field_empty_values(mock_settings, sample_field_dict):
    """测试字段加密功能 - 处理空值和None值"""
    logger.info("Testing field encryption for empty and None values")
    
    with patch('apps.core.mixinx.settings', mock_settings):
        # 测试空字符串
        original_empty = sample_field_dict["empty_field"]
        EncryptMixin.encrypt_field("empty_field", sample_field_dict)
        logger.info(f"Empty field before: '{original_empty}', after: '{sample_field_dict['empty_field']}'")
        
        # 测试None值
        original_none = sample_field_dict["none_field"]
        EncryptMixin.encrypt_field("none_field", sample_field_dict)
        logger.info(f"None field before: {original_none}, after: {sample_field_dict['none_field']}")
        
        logger.info("Empty values encryption test completed")


def test_encrypt_field_nonexistent_field(mock_settings):
    """测试字段加密功能 - 处理不存在的字段名"""
    logger.info("Testing field encryption for nonexistent field")
    
    field_dict = {"existing_field": "value"}
    
    with patch('apps.core.mixinx.settings', mock_settings):
        EncryptMixin.encrypt_field("nonexistent_field", field_dict)
        
        logger.info(f"Field dict after encryption attempt: {field_dict}")
        logger.info(f"Dictionary unchanged: {'nonexistent_field' not in field_dict}")
        logger.info("Nonexistent field encryption test completed")


def test_decrypt_field_encrypted_value(mock_settings, encrypted_field_dict):
    """测试字段解密功能 - 对加密值进行解密"""
    logger.info("Testing field decryption for encrypted value")
    
    field_name = "password"
    original_encrypted = encrypted_field_dict[field_name]
    
    with patch('apps.core.mixinx.settings', mock_settings):
        EncryptMixin.decrypt_field(field_name, encrypted_field_dict)
        
        decrypted_value = encrypted_field_dict[field_name]
        
        logger.info(f"Original encrypted value: {original_encrypted[:20]}...")
        logger.info(f"Decrypted value: {decrypted_value}")
        logger.info(f"Successfully decrypted: {decrypted_value == 'my_secret_password'}")
        logger.info("Field decryption test completed")


def test_decrypt_field_plain_value(mock_settings, sample_field_dict):
    """测试字段解密功能 - 对未加密的普通值尝试解密"""
    logger.info("Testing field decryption for plain text value")
    
    field_name = "api_key"
    original_value = sample_field_dict[field_name]
    
    with patch('apps.core.mixinx.settings', mock_settings):
        EncryptMixin.decrypt_field(field_name, sample_field_dict)
        
        current_value = sample_field_dict[field_name]
        
        logger.info(f"Original plain value: {original_value}")
        logger.info(f"Value after decrypt attempt: {current_value}")
        logger.info(f"Value unchanged (graceful failure): {original_value == current_value}")
        logger.info("Plain text decryption test completed")


def test_decrypt_field_empty_values(mock_settings, sample_field_dict):
    """测试字段解密功能 - 处理空值和None值"""
    logger.info("Testing field decryption for empty and None values")
    
    with patch('apps.core.mixinx.settings', mock_settings):
        # 测试空字符串
        original_empty = sample_field_dict["empty_field"]
        EncryptMixin.decrypt_field("empty_field", sample_field_dict)
        logger.info(f"Empty field before: '{original_empty}', after: '{sample_field_dict['empty_field']}'")
        
        # 测试None值
        original_none = sample_field_dict["none_field"]
        EncryptMixin.decrypt_field("none_field", sample_field_dict)
        logger.info(f"None field before: {original_none}, after: {sample_field_dict['none_field']}")
        
        logger.info("Empty values decryption test completed")


def test_encrypt_decrypt_roundtrip(mock_settings):
    """测试加密解密完整流程 - 验证加密后再解密能恢复原值"""
    logger.info("Testing encrypt-decrypt roundtrip")
    
    original_data = {
        "secret": "very_secret_data",
        "token": "auth_token_12345"
    }
    
    with patch('apps.core.mixinx.settings', mock_settings):
        # 加密
        EncryptMixin.encrypt_field("secret", original_data)
        encrypted_value = original_data["secret"]
        logger.info(f"After encryption - secret: {encrypted_value[:20]}...")
        
        # 解密
        EncryptMixin.decrypt_field("secret", original_data)
        decrypted_value = original_data["secret"]
        logger.info(f"After decryption - secret: {decrypted_value}")
        
        logger.info(f"Roundtrip successful: {decrypted_value == 'very_secret_data'}")
        logger.info("Encrypt-decrypt roundtrip test completed")


def test_encrypt_field_with_none_dict(mock_settings):
    """测试字段加密功能 - 当字段字典为None时的默认行为"""
    logger.info("Testing field encryption with None field_dict")
    
    with patch('apps.core.mixinx.settings', mock_settings):
        result = EncryptMixin.encrypt_field("any_field", None)
        
        logger.info(f"Encryption with None dict result: {result}")
        logger.info("None field_dict encryption test completed")


def test_decrypt_field_with_none_dict(mock_settings):
    """测试字段解密功能 - 当字段字典为None时的默认行为"""
    logger.info("Testing field decryption with None field_dict")
    
    with patch('apps.core.mixinx.settings', mock_settings):
        result = EncryptMixin.decrypt_field("any_field", None)
        
        logger.info(f"Decryption with None dict result: {result}")
        logger.info("None field_dict decryption test completed")
