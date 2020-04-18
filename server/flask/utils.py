import os
from alipay import AliPay
from Crypto.PublicKey import RSA
from base64 import b64decode, b64encode
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto import Random

CUR_PATH = os.path.dirname(__file__)

def decrypt_key(message, privkey=''):
    """
    decrypt the aes_key by the private key
    
    Arguments:
        message {str} -- aes_key
    
    Keyword Arguments:
        privkey {str} -- rsa private key (default: {''})
    
    Returns:
        str -- decrypted aes_key
    """
    
    message = b64decode(message.encode())
    # 读取私钥
    with open(f'{CUR_PATH}/privkey', 'r') as f:
        privkey = RSA.importKey(f.read())
    mlen = len(message)
    dsize = SHA.digest_size
    sentinel = Random.new().read(15 + dsize) 

    priv_cipher = PKCS1_v1_5.new(privkey)
    decipher_text = priv_cipher.decrypt(message, sentinel)
    return b64decode(decipher_text).decode()

def check_trade(out_trade_no=None):
    """
    check trade by the order number
    
    Keyword Arguments:
        out_trade_no {int} -- order number (default: {None})
    
    Returns:
        bool -- decided by trade success or failure
    """
    if not out_trade_no:
        return False
    else:
        app_private_key_string = open(f'{CUR_PATH}/rsa_alipay/app_private.txt').read()
        alipay_public_key_string = open(f'{CUR_PATH}/rsa_alipay/alipay_public.txt').read()
        alipay = AliPay(
            appid="2016102400752486",
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug = True  # 默认False
        )
        try:
            result = alipay.api_alipay_trade_query(out_trade_no=out_trade_no)
        except: 
            pass
        else:
            if result.get("trade_status", "") == "TRADE_SUCCESS":
                return True
            else:
                return False

if __name__ == "__main__":
    s = 'aes_key'
    a = encry_long_key(s)
    print(a)
    t = decrypt_key(a)
    print(t)
