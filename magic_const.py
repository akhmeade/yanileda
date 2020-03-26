# encoding: utf-8

APP_ID = 'f82dd3ae4b2946a6a58b5bcca099bdc0'
APP_SECRET = '71a0be967089402a817b372a857de2ca'

DATETIME_FORMAT = "%Y-%m-%d, %H:%M:%S"

YADISK_PREFIX = "disk:/"

LOCAL_FIL_SYSTEM_NAME = "Local file system"

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

SECURITY_ALGORITMS = ['AES',
                      'Camellia',
                      'ChaCha20',
                      'TipleDES',
                      'CAST5',
                      'SEED']