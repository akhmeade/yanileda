#coding: utf-8
import secrets

def generate_key(length):
    """
    Generate key for encoding
    
    Arguments:
        length {int} -- [length of key in BYTES]
    """
    return secrets.randbits(length * 8).to_bytes(length, "big")