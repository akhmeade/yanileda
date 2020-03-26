# encoding: utf-8
from enum import Enum

APP_ID = 'f82dd3ae4b2946a6a58b5bcca099bdc0'
APP_SECRET = '71a0be967089402a817b372a857de2ca'

DATETIME_FORMAT = "%Y-%m-%d, %H:%M:%S"

YADISK_PREFIX = "disk:/"

LOCAL_FILE_SYSTEM_NAME = "Local file system"

LOCAL_FILE_SYSTEM_LABELS = {
    "message_label":  '''Choose encryption mode for uploading your file to the cloud:''',
    "algorithm_label": "Encryption algorithm:",
    "key_type_label": "Encryption key:",
    "load_button": "Upload file"
}

YADISK_FILE_SYSTEM_LABELS = {
    "message_label":  '''Choose decryption mode for downloading the file from the cloud''',
    "algorithm_label": "Decryption algorithm:",
    "key_type_label": "Dencryption key:",
    "load_button": "Download file"
}

class SecurityAlgorithm(Enum):
    """
        Enumaration class with encryption algorithms
    """
    none = "None"
    aes = "AES"
    camellia = "Camellia"
    chacha20 = "ChaCha20"
    tripleDes = "Triple DES"
    cast5 = "CAST5"
    seed = "SEED"

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