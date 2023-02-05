#Nova Labs
#Modified easycrypt library created by Mark McGookin
#https://github.com/markmcgookin/circuitpython-easycrypt
#Jan 2023

import aesio
from binascii import unhexlify, hexlify

name = "easycrypt"
mode = aesio.MODE_ECB 

def encrypt_string(keystring, inpstring):
    key = bytearray(keystring)
    inp = bytearray(inpstring)
    outp = bytearray(len(inp))
    
    cipher = aesio.AES(key, mode)
    
    cipher.encrypt_into(inp, outp)
    
    trans = hexlify(outp).decode()
    
    return trans

def decrypt_string(keystring, inpstring):
    key = bytearray(keystring)
    inp = bytes(unhexlify(inpstring))
    outp = bytearray(len(inp))
    
    cipher = aesio.AES(key, mode)
    
    cipher.decrypt_into(inp, outp)
    
    trans = outp.decode()
    
    return trans