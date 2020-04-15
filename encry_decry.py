from Crypto.PublicKey import RSA
from base64 import b64decode,b64encode
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto import Random

# 读取密钥
with open('privkey','r') as f:
    privkey = RSA.importKey(f.read())
with open('pubkey','r') as f:
    pubkey = RSA.importKey(f.read())

#加密
def encry_long_key(message, key, max_len = 100, sign = False):
    mlen = len(message)
    cipher = PKCS1_v1_5.new(key)
    h = SHA.new(message)
    result = cipher.encrypt(message+h.digest()) if sign else cipher.encrypt(message)
    return result
#解密
def decrypt_key(message, privkey, max_len = 80):
    mlen = len(message)
    dsize = SHA.digest_size
    sentinel = Random.new().read(15+dsize) 

    priv_cipher = PKCS1_v1_5.new(privkey)
    decipher_text = priv_cipher.decrypt(message, sentinel)
    return decipher_text

#test
a = encry_long_key(b64decode('test'), pubkey)
print(a)

b = decrypt_key(a,privkey)
b= b64encode(b)
print(b)

