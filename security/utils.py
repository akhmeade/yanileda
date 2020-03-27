#coding: utf-8
import os
import base64

def generate_key(length):
    """
    Generate key for encoding
    
    Arguments:
        length {int} -- [length of key in BITS]
    """
    return base64.urlsafe_b64encode(os.urandom(length))
