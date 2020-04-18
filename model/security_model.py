#coding: utf-8

import base64
import os

import sys
# sys.path.append(".")
sys.path.append("f5steganography/")
#print(sys.path)

import magic_const

from magic_const import SecurityAlgorithm
from magic_const import KeyType
from magic_const import MediaType

from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import modes
from cryptography.hazmat.primitives import padding

from f5steganography.utity import embed_into_image
from f5steganography.utity import extract_from_image
from fractals import fractals

from utils import Result

#from test.utity import embed_into_image
#from test.utity import extract_from_image

import logging
logger = logging.getLogger(__name__)

class EchoObject:
    block_size = 8
    def encryptor(self):
        return self
    def decryptor(self):
        return self
    def update(self, text):
        return text
    @property
    def algorithm(self):
        return self


class SecurityModel:
    def __init__(self):
        pass

    def generate_key_by_length(self, length):
        """
        Generate key for encoding
    
        Arguments:
            length {int} -- [length of key in BITS]
        """
        key = base64.urlsafe_b64encode(os.urandom(length))
        return key[:length]
    
    def generate_key(self, alg_type):
        if alg_type == SecurityAlgorithm.none:
            return b""
        else:
            return self.generate_key_by_length(magic_const.KEY_LENGTH[alg_type])

    def browse(self, key_type, algorithm):
        # возможно надо возвращать словарь с инфой что делать
        # типа если просто ключ, то например
        # {"action": "show", "key": key}
        # а если там надо путь указывать
        # {"action": "get_file_name", "limits": "jpg, png"}
        # и потом view решает что делать
        
        if  key_type == KeyType.new_symbols:
            key = self.generate_key(algorithm)
            return {"action": "show",
                "key": key.decode("utf-8")}
                
        elif key_type == KeyType.existing_symbols:
            return {"action": "nothing"}

        elif key_type == KeyType.new_media:
            return {"action": "get_open_filename",
                "limits" : "Images (*.png *.jpg)"}
        
        elif key_type == KeyType.existing_media:
            return {"action": "get_open_filename",
                "limits" : "Images (*.png *.jpg)"}
        
        elif key_type == KeyType.new_binary:
                return {"action": "get_save_filename",
                "limits" : "Binary file (*.key)"}
        
        elif key_type == KeyType.existing_binary:
            return {"action": "get_open_filename",
                "limits" : "Binary file (*.key)"}

    def encrypt(self, from_path, to_path, encryption_data):
        cipher = self.get_cipher(encryption_data)
        if not cipher.is_ok():
            return cipher
        cipher = cipher.result()
        encrypter = cipher.encryptor()
        block_size = cipher.algorithm.block_size

        padder = padding.PKCS7(block_size).padder()

        with open(from_path, "rb") as file:
            data = file.read()

        padded_data = padder.update(data)
        padded_data += padder.finalize()
        crypted = encrypter.update(padded_data)

        with open(to_path, "wb") as file:
            file.write(crypted)
        #self.update(encrypter, from_path, to_path, padder.padder())
    
    def decrypt(self, from_path, to_path, encryption_data):
        cipher = self.get_cipher(encryption_data)
        if not cipher.is_ok():
            return cipher
        cipher = cipher.result()
        decryptor = cipher.decryptor()
        block_size = cipher.algorithm.block_size

        padder = padding.PKCS7(block_size).unpadder()

        with open(from_path, "rb") as file:
            data = file.read()

        crypted = decryptor.update(data)

        padded_data = padder.update(crypted)
        padded_data += padder.finalize()
                
        with open(to_path, "wb") as file:
            file.write(padded_data)
        #self.update(decryptor, from_path, to_path, padder.unpadder())

    # def update(self, crypter, from_path, to_path, padder):
    #     with open(from_path, "rb") as file:
    #         data = file.read()
    #     #print(data)
    #     crypted = crypter.update(padded_data)
    #     print(len(padded_data), len(crypted))
    #     #print(crypted)
    #     with open(to_path, "wb") as file:
    #         file.write(crypted)

    def get_cipher(self, crypto_data):
        #assert len(encryption_data) == 4
        algorithm_type = crypto_data["algorithm"]
        key_type = crypto_data["key_type"]
        media_path = crypto_data["media_path"]
        key = crypto_data["key"]
        media_type = crypto_data["media_type"]

        # get key from media if need it
        if algorithm_type != SecurityAlgorithm.none:
            key = self.get_key(algorithm_type, key_type, key, media_path, media_type)
            if not key.is_ok():
                return key
            else:
                key = key.result()

        algorithm = self.get_algorithm(algorithm_type, key)

        if algorithm is None:
            cipher = EchoObject()
        else:
            cipher = Cipher(algorithm, mode=modes.ECB(), backend=default_backend())
            #print(cipher.algorithm.block_size)
            #print(cipher.block_size)

        return Result.success(cipher)


    def get_algorithm(self, algorithm, key):
        if algorithm == SecurityAlgorithm.none:
            return None
        elif algorithm == SecurityAlgorithm.aes:
            return algorithms.AES(key)
        elif algorithm == SecurityAlgorithm.camellia:
            return algorithms.Camellia(key)
        #elif algorithm == SecurityAlgorithm.chacha20:
        #    return algorithms.ChaCha20(key)
        elif algorithm == SecurityAlgorithm.triple_des:
            return algorithms.TripleDES(key)
        elif algorithm == SecurityAlgorithm.cast5:
            return algorithms.CAST5(key)
        elif algorithm == SecurityAlgorithm.seed:
            return algorithms.SEED(key)
        else:
            logger.error("Not supportable algorithm")

    def get_key(self, algorithm_type, key_type, key, media_path, media_type):
        logger.info("Key-file path %s" % media_path)
        if key_type == KeyType.new_symbols:
            if not key:
                return Result.failed("Empty key")
            return Result.success(key)
        
        elif key_type == KeyType.existing_symbols:
            if not key:
                return Result.failed("Empty key")
            return Result.success(key)
        
        elif key_type == KeyType.new_binary:
            if not media_path:
                return Result.failed("Empty file path")
            
            key = self.generate_key(algorithm_type)
            with open(media_path, "wb") as f:
                f.write(key)
            return Result.success(key)
        
        elif key_type == KeyType.existing_binary:
            if not media_path:
                return Result.failed("Empty file path")

            with open(media_path, "rb") as f:
                key = f.read()
            return key

        elif key_type == KeyType.new_media:
            
            if not key:
                return Result.failed("Empty key")
            if not media_path:
                return Result.failed("Empty media path")
            if media_type == MediaType.f5steganography:
                key_key = self.generate_key(algorithm_type)
                embed_into_image(media_path, key_key.decode("utf-8"), key)
            elif media_type == MediaType.fractals:
                key_size = magic_const.KEY_LENGTH[algorithm_type]
                key_key = fractals.generate_key(media_path, key.decode("utf-8"), key_size)
            else:
                logger.error("Bad media type %s" % media_type)
            return Result.success(key_key)
            
        elif key_type == KeyType.existing_media:
            return extract_from_image(media_path, key)
    
    def get_key_for_presenter(self, algorithm, key_type):
        if key_type == KeyType.new_symbols:
            return self.generate_key(algorithm).decode("utf-8")
        else:
            return ""