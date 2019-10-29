## Rafael Sartori M. Santos, 186154
##
## Programa de utilidades para codificar e decodificar

# Modificado de https://www.quickprogrammingtips.com/python/aes-256-encryption-and-decryption-in-python.html

from Crypto.Cipher import AES # algoritmo AES
from Crypto.Protocol.KDF import PBKDF2 # para hashing seguro de senhas
from Crypto.Util.Padding import pad, unpad # para padding dos blocos de 16 bytes

BLOCK_SIZE = 16
SALT = b"LFstPpN1fTIEbTcIuNja1hLzZEE="

def _get_pbkdf2_key(password):
    # Pegamos a chave de PBKDF2 (apenas 32 bytes)
    return PBKDF2(password, SALT, 64, 1000)[:32]

def aes_encrypt(data, password):
    # Pegamos uma chave de 32 bytes
    private_key = _get_pbkdf2_key(password)
    # Fazemos o cipher
    cipher = AES.new(private_key, AES.MODE_CBC)
    # Retornamos o vetor inicial com a mensagem cifrada
    return cipher.iv + cipher.encrypt(pad(data, AES.block_size))

def aes_decrypt(data, password):
    # Pegamos uma chave de 32 bytes
    private_key = _get_pbkdf2_key(password)
    # Pegamos o IV
    iv = data[:16]
    # Fazemos o cipher
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    # Deciframos
    return unpad(cipher.decrypt(data[16:]), AES.block_size)


