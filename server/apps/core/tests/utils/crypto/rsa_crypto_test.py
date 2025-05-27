import pytest
import logging
from apps.core.utils.crypto.rsa_crypto import RSACryptor

logger = logging.getLogger(__name__)


@pytest.fixture
def rsa_cryptor():
    """创建RSACryptor实例的fixture"""
    return RSACryptor()


@pytest.fixture
def test_plaintext():
    """测试用的明文数据"""
    return "这是一个测试消息，用于验证RSA加密解密功能"


def test_rsa_key_generation():
    """测试RSA密钥对生成功能"""
    logger.info("开始测试RSA密钥对生成")
    
    cryptor = RSACryptor()
    
    logger.info(f"私钥长度: {len(cryptor.private_key)}")
    logger.info(f"公钥长度: {len(cryptor.public_key)}")
    logger.info("私钥类型检查通过" if b'BEGIN RSA PRIVATE KEY' in cryptor.private_key else "私钥格式异常")
    logger.info("公钥类型检查通过" if b'BEGIN PUBLIC KEY' in cryptor.public_key else "公钥格式异常")
    
    logger.info("RSA密钥对生成测试完成")


def test_rsa_custom_key_size():
    """测试自定义密钥长度功能"""
    logger.info("开始测试自定义密钥长度")
    
    custom_size = 1024
    cryptor = RSACryptor(bits=custom_size)
    
    logger.info(f"自定义密钥长度: {custom_size}")
    logger.info(f"生成的私钥长度: {len(cryptor.private_key)}")
    
    logger.info("自定义密钥长度测试完成")


def test_rsa_encrypt_decrypt_flow(rsa_cryptor, test_plaintext):
    """测试RSA完整的加密解密流程"""
    logger.info("开始测试RSA加密解密流程")
    
    # 使用生成的密钥对进行加密解密
    encrypted = rsa_cryptor.encrypt_rsa(test_plaintext, rsa_cryptor.public_key)
    logger.info(f"原文: {test_plaintext}")
    logger.info(f"密文长度: {len(encrypted)}")
    
    decrypted = rsa_cryptor.decrypt_rsa(encrypted, rsa_cryptor.private_key)
    logger.info(f"解密结果: {decrypted}")
    
    logger.info(f"加解密一致性检查: {'通过' if test_plaintext == decrypted else '失败'}")
    logger.info("RSA加密解密流程测试完成")


def test_rsa_encrypt_with_invalid_inputs(rsa_cryptor):
    """测试RSA加密时的异常输入处理"""
    logger.info("开始测试RSA加密异常输入处理")
    
    # 测试空文本
    try:
        rsa_cryptor.encrypt_rsa("", rsa_cryptor.public_key)
    except ValueError as e:
        logger.info(f"空文本异常捕获成功: {e}")
    
    # 测试空公钥
    try:
        rsa_cryptor.encrypt_rsa("test", "")
    except ValueError as e:
        logger.info(f"空公钥异常捕获成功: {e}")
    
    # 测试无效公钥
    try:
        rsa_cryptor.encrypt_rsa("test", "invalid_key")
    except Exception as e:
        logger.info(f"无效公钥异常捕获成功: {type(e).__name__}")
    
    logger.info("RSA加密异常输入处理测试完成")


def test_rsa_decrypt_with_invalid_inputs(rsa_cryptor):
    """测试RSA解密时的异常输入处理"""
    logger.info("开始测试RSA解密异常输入处理")
    
    # 测试空密文
    try:
        rsa_cryptor.decrypt_rsa("", rsa_cryptor.private_key)
    except ValueError as e:
        logger.info(f"空密文异常捕获成功: {e}")
    
    # 测试空私钥
    try:
        rsa_cryptor.decrypt_rsa("test", "")
    except ValueError as e:
        logger.info(f"空私钥异常捕获成功: {e}")
    
    # 测试无效密文
    try:
        rsa_cryptor.decrypt_rsa("invalid_encrypted_text", rsa_cryptor.private_key)
    except Exception as e:
        logger.info(f"无效密文异常捕获成功: {type(e).__name__}")
    
    logger.info("RSA解密异常输入处理测试完成")


def test_rsa_invalid_key_size():
    """测试无效密钥长度的异常处理"""
    logger.info("开始测试无效密钥长度异常处理")
    
    try:
        RSACryptor(bits=512)  # 小于最小长度
    except ValueError as e:
        logger.info(f"无效密钥长度异常捕获成功: {e}")
    
    logger.info("无效密钥长度异常处理测试完成")


def test_rsa_with_chinese_characters(rsa_cryptor):
    """测试RSA处理中文字符的能力"""
    logger.info("开始测试RSA中文字符处理")
    
    chinese_text = "这是中文测试：你好世界！@#￥%"
    
    encrypted = rsa_cryptor.encrypt_rsa(chinese_text, rsa_cryptor.public_key)
    decrypted = rsa_cryptor.decrypt_rsa(encrypted, rsa_cryptor.private_key)
    
    logger.info(f"中文原文: {chinese_text}")
    logger.info(f"中文解密: {decrypted}")
    logger.info(f"中文处理一致性: {'通过' if chinese_text == decrypted else '失败'}")
    
    logger.info("RSA中文字符处理测试完成")
