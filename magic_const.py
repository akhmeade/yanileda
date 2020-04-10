# encoding: utf-8
from enum import Enum

APP_ID = 'f82dd3ae4b2946a6a58b5bcca099bdc0'
APP_SECRET = '71a0be967089402a817b372a857de2ca'

DATETIME_FORMAT = "%Y-%m-%d, %H:%M:%S"

YADISK_PREFIX = "disk:/"

LOCAL_FILE_SYSTEM_NAME = "Local file system"


class KeyType(Enum):
    """
        Enumaration class with encryption key types
    """
    new_symbols = "New key as symbols"
    new_binary = "New key for binary file"
    new_media = "New key for media"
    existing_symbols = "Existing symbols"
    existing_binary = "Existing binary file"
    existing_media = "Existing media"

LOCAL_FILE_SYSTEM_LABELS = {
    "message_label":  '''Choose encryption mode for uploading your file to the cloud:''',
    "algorithm_label": "Encryption algorithm:",
    "key_type_label": "Encryption key:",
    "load_button": "Upload file",
    "key_type": [KeyType.new_symbols, KeyType.new_binary, KeyType.new_media,
         KeyType.existing_symbols, KeyType.existing_binary, KeyType.existing_media]
}

YADISK_FILE_SYSTEM_LABELS = {
    "message_label":  '''Choose decryption mode for downloading the file from the cloud''',
    "algorithm_label": "Decryption algorithm:",
    "key_type_label": "Dencryption key:",
    "load_button": "Download file",
    "key_type": [KeyType.existing_symbols, KeyType.existing_binary, KeyType.existing_media]
}

class SecurityAlgorithm(Enum):
    """
        Enumaration class with encryption algorithms
    """
    none = "None"
    aes = "AES"
    camellia = "Camellia"
    chacha20 = "ChaCha20"
    triple_des = "Triple DES"
    cast5 = "CAST5"
    seed = "SEED"

KEY_LENGTH = {
    SecurityAlgorithm.aes: 32,
    SecurityAlgorithm.camellia: 32,
    SecurityAlgorithm.chacha20: 32,
    SecurityAlgorithm.triple_des: 24,
    SecurityAlgorithm.cast5: 16,
    SecurityAlgorithm.seed: 16
}