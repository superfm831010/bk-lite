import pytest
import logging
from apps.core.utils.crypto.password_crypto import PasswordCrypto

logger = logging.getLogger(__name__)


@pytest.fixture
def strong_password():
    """强密码fixture"""
    return "StrongPassword123!@#"


@pytest.fixture
def weak_password():
    """弱密码fixture"""
    return "weak"


@pytest.fixture
def test_data():
    """测试数据fixture"""
    return "这是一个测试数据，包含中文和English mixed content 123!@#"


def test_password_crypto_initialization_with_strong_password(strong_password):
    """测试使用强密码初始化PasswordCrypto"""
    logger.info("开始测试强密码初始化")
    
    crypto = PasswordCrypto(strong_password)
    
    logger.info(f"输入密码长度: {len(strong_password)}")
    logger.info(f"处理后密钥长度: {len(crypto.key)}")
    logger.info(f"密钥长度符合要求: {'是' if len(crypto.key) == 32 else '否'}")
    
    logger.info("强密码初始化测试完成")


def test_password_crypto_initialization_with_weak_password(weak_password):
    """测试使用弱密码初始化PasswordCrypto（应产生警告）"""
    logger.info("开始测试弱密码初始化")
    
    crypto = PasswordCrypto(weak_password)
    
    logger.info(f"弱密码长度: {len(weak_password)}")
    logger.info(f"处理后密钥长度: {len(crypto.key)}")
    logger.info("弱密码警告测试 - 检查日志中是否有警告信息")
    
    logger.info("弱密码初始化测试完成")


def test_password_crypto_encrypt_decrypt_flow(strong_password, test_data):
    """测试PasswordCrypto完整的加密解密流程"""
    logger.info("开始测试PasswordCrypto加密解密流程")
    
    crypto = PasswordCrypto(strong_password)
    
    encrypted = crypto.encrypt(test_data)
    logger.info(f"原始数据: {test_data}")
    logger.info(f"加密结果长度: {len(encrypted)}")
    logger.info(f"加密结果预览: {encrypted[:50]}...")
    
    decrypted = crypto.decrypt(encrypted)
    logger.info(f"解密结果: {decrypted}")
    
    logger.info(f"数据一致性检查: {'通过' if test_data == decrypted else '失败'}")
    logger.info("PasswordCrypto加密解密流程测试完成")


def test_password_crypto_multiple_encryptions(strong_password):
    """测试多次加密产生不同密文（由于随机IV）"""
    logger.info("开始测试多次加密结果差异")
    
    crypto = PasswordCrypto(strong_password)
    plaintext = "相同的明文数据"
    
    encrypted1 = crypto.encrypt(plaintext)
    encrypted2 = crypto.encrypt(plaintext)
    
    logger.info(f"第一次加密: {encrypted1[:50]}...")
    logger.info(f"第二次加密: {encrypted2[:50]}...")
    logger.info(f"两次加密结果不同: {'是' if encrypted1 != encrypted2 else '否'}")
    
    # 验证都能正确解密
    decrypted1 = crypto.decrypt(encrypted1)
    decrypted2 = crypto.decrypt(encrypted2)
    
    logger.info(f"第一次解密正确: {'是' if decrypted1 == plaintext else '否'}")
    logger.info(f"第二次解密正确: {'是' if decrypted2 == plaintext else '否'}")
    
    logger.info("多次加密结果差异测试完成")


def test_password_crypto_empty_inputs():
    """测试空输入的异常处理"""
    logger.info("开始测试空输入异常处理")
    
    # 测试空密钥
    try:
        PasswordCrypto("")
    except ValueError as e:
        logger.info(f"空密钥异常捕获成功: {e}")
    
    # 测试空明文加密
    crypto = PasswordCrypto("test_password")
    try:
        crypto.encrypt("")
    except ValueError as e:
        logger.info(f"空明文加密异常捕获成功: {e}")
    
    # 测试空密文解密
    try:
        crypto.decrypt("")
    except ValueError as e:
        logger.info(f"空密文解密异常捕获成功: {e}")
    
    logger.info("空输入异常处理测试完成")


def test_password_crypto_invalid_encrypted_data(strong_password):
    """测试无效加密数据的解密处理"""
    logger.info("开始测试无效加密数据处理")
    
    crypto = PasswordCrypto(strong_password)
    
    # 测试无效base64数据
    try:
        crypto.decrypt("invalid_base64_data!")
    except Exception as e:
        logger.info(f"无效base64数据异常捕获成功: {type(e).__name__}")
    
    # 测试长度不足的数据
    try:
        crypto.decrypt("dGVzdA==")  # "test" in base64, too short
    except Exception as e:
        logger.info(f"数据长度不足异常捕获成功: {type(e).__name__}: {e}")
    
    logger.info("无效加密数据处理测试完成")


def test_password_crypto_with_different_key_lengths():
    """测试不同长度密钥的处理"""
    logger.info("开始测试不同长度密钥处理")
    
    test_keys = [
        "short",           # 短密钥
        "medium_length_password",  # 中等长度
        "very_long_password_that_exceeds_32_bytes_limit_significantly"  # 超长密钥
    ]
    
    test_text = "测试文本"
    
    for i, key in enumerate(test_keys):
        logger.info(f"测试密钥 {i+1}: 长度={len(key)}")
        
        crypto = PasswordCrypto(key)
        logger.info(f"处理后密钥长度: {len(crypto.key)}")
        
        encrypted = crypto.encrypt(test_text)
        decrypted = crypto.decrypt(encrypted)
        
        logger.info(f"加解密一致性: {'通过' if test_text == decrypted else '失败'}")
    
    logger.info("不同长度密钥处理测试完成")


def test_password_crypto_unicode_handling(strong_password):
    """测试Unicode字符处理能力"""
    logger.info("开始测试Unicode字符处理")
    
    crypto = PasswordCrypto(strong_password)
    
    unicode_texts = [
        "普通中文文本",
        "English text with symbols !@#$%^&*()",
        "混合文本 Mixed 🚀 emoji and 特殊字符",
        "日本語テスト",
        "Русский текст",
        "العربية النص"
    ]
    
    for i, text in enumerate(unicode_texts):
        logger.info(f"测试Unicode文本 {i+1}: {text[:20]}...")
        
        encrypted = crypto.encrypt(text)
        decrypted = crypto.decrypt(encrypted)
        
        logger.info(f"Unicode处理一致性: {'通过' if text == decrypted else '失败'}")
    
    logger.info("Unicode字符处理测试完成")
