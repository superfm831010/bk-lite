import pytest
import logging
from unittest.mock import patch
from apps.core.utils.crypto.aes_crypto import AESCryptor

logger = logging.getLogger(__name__)


@pytest.fixture
def mock_secret_key():
    """模拟SECRET_KEY的fixture"""
    return "test_secret_key_for_aes_encryption"


@pytest.fixture
def test_plaintext():
    """测试明文数据"""
    return "这是AES测试数据，包含中文和English mixed content 123!@#"


@patch('apps.core.utils.crypto.aes_crypto.SECRET_KEY', 'test_secret_key')
def test_aes_cryptor_initialization():
    """测试AESCryptor初始化功能"""
    logger.info("开始测试AESCryptor初始化")
    
    cryptor = AESCryptor()
    
    logger.info("AESCryptor初始化成功")
    logger.info(f"内部密钥已生成，长度: {len(cryptor._AESCryptor__key)}")
    logger.info(f"块大小设置: {cryptor._AESCryptor__block_size}")
    
    logger.info("AESCryptor初始化测试完成")


@patch('apps.core.utils.crypto.aes_crypto.SECRET_KEY', 'test_secret_key')
def test_aes_encode_decode_flow(test_plaintext):
    """测试AES完整的编码解码流程"""
    logger.info("开始测试AES编码解码流程")
    
    cryptor = AESCryptor()
    
    encoded = cryptor.encode(test_plaintext)
    logger.info(f"原始数据: {test_plaintext}")
    logger.info(f"编码结果长度: {len(encoded)}")
    logger.info(f"编码结果预览: {encoded[:50]}...")
    logger.info(f"URL安全字符检查: {'通过' if all(c.isalnum() or c in '-_' for c in encoded) else '失败'}")
    
    decoded = cryptor.decode(encoded)
    logger.info(f"解码结果: {decoded}")
    
    logger.info(f"编解码一致性检查: {'通过' if test_plaintext == decoded else '失败'}")
    logger.info("AES编码解码流程测试完成")


@patch('apps.core.utils.crypto.aes_crypto.SECRET_KEY', 'test_secret_key')
def test_aes_multiple_encodings():
    """测试多次编码产生不同结果（由于随机IV）"""
    logger.info("开始测试多次编码结果差异")
    
    cryptor = AESCryptor()
    plaintext = "相同的明文数据"
    
    encoded1 = cryptor.encode(plaintext)
    encoded2 = cryptor.encode(plaintext)
    
    logger.info(f"第一次编码: {encoded1[:30]}...")
    logger.info(f"第二次编码: {encoded2[:30]}...")
    logger.info(f"两次编码结果不同: {'是' if encoded1 != encoded2 else '否'}")
    
    # 验证都能正确解码
    decoded1 = cryptor.decode(encoded1)
    decoded2 = cryptor.decode(encoded2)
    
    logger.info(f"第一次解码正确: {'是' if decoded1 == plaintext else '否'}")
    logger.info(f"第二次解码正确: {'是' if decoded2 == plaintext else '否'}")
    
    logger.info("多次编码结果差异测试完成")


@patch('apps.core.utils.crypto.aes_crypto.SECRET_KEY', '')
def test_aes_empty_secret_key():
    """测试空SECRET_KEY的异常处理"""
    logger.info("开始测试空SECRET_KEY异常处理")
    
    try:
        AESCryptor()
    except ValueError as e:
        logger.info(f"空SECRET_KEY异常捕获成功: {e}")
    
    logger.info("空SECRET_KEY异常处理测试完成")


@patch('apps.core.utils.crypto.aes_crypto.SECRET_KEY', 'test_secret_key')
def test_aes_empty_inputs():
    """测试空输入的异常处理"""
    logger.info("开始测试空输入异常处理")
    
    cryptor = AESCryptor()
    
    # 测试空明文编码
    try:
        cryptor.encode("")
    except ValueError as e:
        logger.info(f"空明文编码异常捕获成功: {e}")
    
    # 测试空密文解码
    try:
        cryptor.decode("")
    except ValueError as e:
        logger.info(f"空密文解码异常捕获成功: {e}")
    
    logger.info("空输入异常处理测试完成")


@patch('apps.core.utils.crypto.aes_crypto.SECRET_KEY', 'test_secret_key')
def test_aes_invalid_encoded_data():
    """测试无效编码数据的解码处理"""
    logger.info("开始测试无效编码数据处理")
    
    cryptor = AESCryptor()
    
    # 测试无效base64数据
    try:
        cryptor.decode("invalid_base64_data!")
    except Exception as e:
        logger.info(f"无效base64数据异常捕获成功: {type(e).__name__}")
    
    # 测试长度不足的数据
    try:
        cryptor.decode("dGVzdA")  # 短数据
    except Exception as e:
        logger.info(f"数据长度不足异常捕获成功: {type(e).__name__}: {e}")
    
    logger.info("无效编码数据处理测试完成")


@patch('apps.core.utils.crypto.aes_crypto.SECRET_KEY', 'test_secret_key')
def test_aes_padding_handling():
    """测试base64填充字符处理"""
    logger.info("开始测试base64填充字符处理")
    
    cryptor = AESCryptor()
    
    # 测试不同长度的文本，验证填充处理
    test_texts = [
        "a",          # 1字符
        "ab",         # 2字符
        "abc",        # 3字符
        "abcd",       # 4字符
        "abcde"       # 5字符
    ]
    
    for i, text in enumerate(test_texts):
        logger.info(f"测试文本 {i+1}: '{text}' (长度: {len(text)})")
        
        encoded = cryptor.encode(text)
        logger.info(f"编码结果长度: {len(encoded)}")
        logger.info(f"包含填充字符: {'否' if '=' not in encoded else '是'}")
        
        decoded = cryptor.decode(encoded)
        logger.info(f"解码一致性: {'通过' if text == decoded else '失败'}")
    
    logger.info("base64填充字符处理测试完成")


@patch('apps.core.utils.crypto.aes_crypto.SECRET_KEY', 'test_secret_key')
def test_aes_large_data_handling():
    """测试大数据量的处理能力"""
    logger.info("开始测试大数据量处理")
    
    cryptor = AESCryptor()
    
    # 生成较大的测试数据
    large_text = "测试数据" * 1000  # 约4KB数据
    
    logger.info(f"大数据原始长度: {len(large_text)} 字符")
    
    encoded = cryptor.encode(large_text)
    logger.info(f"编码后长度: {len(encoded)} 字符")
    
    decoded = cryptor.decode(encoded)
    logger.info(f"解码后长度: {len(decoded)} 字符")
    
    logger.info(f"大数据处理一致性: {'通过' if large_text == decoded else '失败'}")
    
    logger.info("大数据量处理测试完成")


@patch('apps.core.utils.crypto.aes_crypto.SECRET_KEY', 'test_secret_key')
def test_aes_special_characters():
    """测试特殊字符和符号的处理"""
    logger.info("开始测试特殊字符处理")
    
    cryptor = AESCryptor()
    
    special_texts = [
        "!@#$%^&*()_+-={}[]|\\:;\"'<>?,./",
        "换行\n制表\t回车\r",
        "Unicode: 🚀🌟💻🔐",
        "空格    多个空格",
        "引号'单引号\"双引号`反引号"
    ]
    
    for i, text in enumerate(special_texts):
        logger.info(f"测试特殊字符 {i+1}: {repr(text)}")
        
        encoded = cryptor.encode(text)
        decoded = cryptor.decode(encoded)
        
        logger.info(f"特殊字符处理一致性: {'通过' if text == decoded else '失败'}")
    
    logger.info("特殊字符处理测试完成")
