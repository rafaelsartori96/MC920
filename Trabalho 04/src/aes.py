## Rafael Sartori M. Santos, 186154
##
## Programa de utilidades para codificar e decodificar

# Modificado de https://www.quickprogrammingtips.com/python/aes-256-encryption-and-decryption-in-python.html

from Crypto.Cipher import AES # algoritmo AES
from Crypto import Random # iniciar o initializing vector usado em AES
from Crypto.Protocol.KDF import PBKDF2 # para hashing seguro de senhas

BLOCK_SIZE = 16
SALT = b"LFstPpN1fTIEbTcIuNja1hLzZEE="

def _pad(string):
    return string + (BLOCK_SIZE - len(string) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(string) % BLOCK_SIZE)

def _unpad(string):
    return string[:-ord(string[len(string) - 1:])]

def _get_pbkdf2_key(password):
    # Pegamos a chave de PBKDF2 (apenas 32 bytes)
    return PBKDF2(password, SALT, 64, 1000)[:32]

def aes_encrypt(data, password):
    # Pegamos uma chave de 32 bytes
    private_key = _get_pbkdf2_key(password)
    # Pegamos um IV aleatório
    iv = Random.new().read(AES.block_size)
    # Fazemos o cipher
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    # Colocamos o IV no início
    return iv + cipher.encrypt(_pad(data))

def aes_decrypt(data, password):
    # Pegamos uma chave de 32 bytes
    private_key = _get_pbkdf2_key(password)
    # Pegamos o IV
    iv = data[:16]
    # Fazemos o cipher
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    # Deciframos
    return _unpad(cipher.decrypt(data[16:]))

