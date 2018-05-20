from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class Const:
    END_OF_REC = b'__e__'
    UTF8_ENC = 'utf-8'
    REC_TOKENS_SEP = '__'
    B_REC_TOKENS_SEP = bytes(REC_TOKENS_SEP, encoding=UTF8_ENC)
    BLOCK_SIZE = 128


class Globals:
    db_data = dict()
    db_file = None


class Utils:
    """Cipher Info
    Cipher      - AES
    Key size    - 256-bit
    Block size  - 128-bit
    IV          - 128 bit
    """

    cipher = None
    # TODO - iv should not be static
    iv = b'\xcf\xbe\x04\xb5\xbc\x9bs\x92r\xe6\x98\xe5e/\xee\xd4'

    @staticmethod
    def init_cipher(key):
        global cipher
        cipher = Cipher(algorithms.AES(key[:32].encode(encoding=Const.UTF8_ENC)),
                        modes.CBC(Utils.iv),
                        backend=default_backend())

    @staticmethod
    def get_hash(in_str):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(in_str.encode(encoding=Const.UTF8_ENC))
        raw_digest = digest.finalize()
        return bytes(raw_digest).hex()

    @staticmethod
    def encrypt(plain_str):
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(Const.BLOCK_SIZE).padder()
        padded_data = padder.update(plain_str.encode(encoding=Const.UTF8_ENC)) + padder.finalize()
        return encryptor.update(padded_data) + encryptor.finalize()

    @staticmethod
    def decrypt(cipher_str):
        decryptor = cipher.decryptor()
        plain_unpadded_str = decryptor.update(cipher_str) + decryptor.finalize()
        unpadder = padding.PKCS7(Const.BLOCK_SIZE).unpadder()
        return unpadder.update(plain_unpadded_str) + unpadder.finalize()
