from Crypto.PublicKey import RSA
from base64 import b64decode,b64encode
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto import Random

def encry_long_key(message, pubkey='', max_len = 100, sign = False):
    ''' 加密函数 '''
    # 读取公钥
    with open('pubkey', 'r') as f:
        pubkey = RSA.importKey(f.read())
    mlen = len(message)
    cipher = PKCS1_v1_5.new(pubkey)
    h = SHA.new(message)
    result = cipher.encrypt(message + h.digest()) if sign else cipher.encrypt(message)
    return b64encode(result).decode()

def decrypt_key(message, privkey='', max_len = 80):
    ''' 解密函数 '''
    message = b64decode(message)
    # 读取私钥
    with open('privkey', 'r') as f:
        privkey = RSA.importKey(f.read())
    mlen = len(message)
    dsize = SHA.digest_size
    sentinel = Random.new().read(15 + dsize) 

    priv_cipher = PKCS1_v1_5.new(privkey)
    decipher_text = priv_cipher.decrypt(message, sentinel)
    return b64encode(decipher_text).decode()

if __name__ == "__main__":
    a = encry_long_key(b64decode('test'))
    print(a)
    # print(b64encode(a).decode())
    # print(b64decode(b64encode(a).decode()))
    # print(type(b64encode(a).decode()))
    b = decrypt_key(a)
    print(b)
