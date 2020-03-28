#coding: utf-8

import base64
import os

import magic_const
from magic_const import KeyType

class SecurityModel:

    def generate_key(self, length):
        """
        Generate key for encoding
    
        Arguments:
            length {int} -- [length of key in BITS]
        """
        return base64.urlsafe_b64encode(os.urandom(length))

    def browse(self, key_type):
        # возможно надо возвращать словарь с инфой что делать
        # типа если просто ключ, то например
        # {"action": "show", "key": key}
        # а если там надо путь указывать
        # {"action": "get_file_name", "limits": "jpg, png"}
        # и потом view решает что делать
        
        if  key_type == KeyType.new_symbols:
            key = self.generate_key(magic_const.SYMBOL_KEY_LENGTH)
            return key.decode("utf-8")
        
