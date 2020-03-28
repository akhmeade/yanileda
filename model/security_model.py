#coding: utf-8

import base64
import os

class SecurityModel:

    def generate_key(self, length):
            """
        Generate key for encoding
    
        Arguments:
            length {int} -- [length of key in BITS]
        """
        return base64.urlsafe_b64encode(os.urandom(length))