import os

import logging

logger = logging.getLogger(__name__)

from src.core.sanic_plus.utils.crypto import PasswordCrypto


def test_decrypt():
    crypto = PasswordCrypto(os.getenv("SECRET_KEY"))
    rs = crypto.encrypt(os.getenv("ADMIN_PASSWORD"))
    logger.info(rs)
    result = crypto.decrypt(rs)
    logger.info(result)
