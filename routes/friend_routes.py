# from flask import Blueprint, request, jsonify
# from services.friend_service import send_friend_request, respond_friend_request, get_friends_list

# friend_bp = Blueprint('friend', __name__)

# @friend_bp.route('/friends', methods=['GET'])
# def friends():
#     user_id = request.args.get('user_id')
#     return get_friends_list(user_id)

# @friend_bp.route('/friends/request', methods=['POST'])
# def request_friend():
#     data = request.get_json()
#     return send_friend_request(data)

# @friend_bp.route('/friends/respond', methods=['POST'])
# def respond_friend():
#     data = request.get_json()
#     return respond_friend_request(data)

from flask import Blueprint, request, jsonify
from flasgger import Swagger, swag_from
from services.friend_service import send_friend_request, respond_friend_request, get_friends_list
import logging
from utils.helpers import authorize
from flask import g

friend_bp = Blueprint('friend', __name__)
logger = logging.getLogger(__name__)

@friend_bp.route('/friends', methods=['GET'])
@authorize(allowed_user_types=['user','artist'])
@swag_from({
    'tags': ['Friends'],
    'security': [{'Bearer': []}],
    'responses': {
        200: {
            'description': 'A list of friends',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'friend_id': {'type': 'integer'},
                        'request_user_id': {'type': 'integer'},
                        'response_user_id': {'type': 'integer'},
                        'status': {'type': 'string'},
                        'created_at': {'type': 'string', 'format': 'date-time'},
                        'updated_at': {'type': 'string', 'format': 'date-time'},
                        'is_active': {'type': 'boolean'}
                    }
                }
            }
        }
    }
})
def friends(current_user):
    """
    Get a list of friends for a user
    ---
    parameters:
      - name: user_id
        in: query
        type: integer
        required: true
        description: The ID of the user
    responses:
      200:
        description: A list of friends
    """
    user_id = request.args.get('user_id')
    if str(user_id) == str(g.user_id):
        return get_friends_list(user_id)
    else:
        return jsonify({'message': 'Invalid request'}), 403
    

@friend_bp.route('/friends/request', methods=['POST'])
@authorize(allowed_user_types=['user','artist'])
@swag_from({
    'tags': ['Friends'],
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'request_user_id': {'type': 'integer', 'example': 1},
                    'response_user_id': {'type': 'integer', 'example': 2}
                },
                'required': ['request_user_id', 'response_user_id']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Friend request sent successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        }
    }
})
def request_friend(current_user):
     
    data = request.get_json()
    logger.debug(f"send_friend_request called with data: {data}")
    request_user_id = data['request_user_id']
    response_user_id = data['response_user_id']
    logger.info(f"Friend request request_user_id {request_user_id} and response_user_id {response_user_id} and global user {g.user_id}")
           
    if str(request_user_id) == str(g.user_id) and request_user_id!=response_user_id:
        return send_friend_request(data)
    else:
        return jsonify({'message': 'Invalid request'}), 403
    

@friend_bp.route('/friends/respond', methods=['POST'])
@authorize(allowed_user_types=['user','artist'])
@swag_from({
    'tags': ['Friends'],
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'request_user_id': {'type': 'integer', 'example': 1},
                    'response_user_id': {'type': 'integer', 'example': 2},
                    'status': {'type': 'string', 'example': 'accepted'}
                },
                'required': ['request_user_id', 'response_user_id', 'status']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Friend request response updated successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        },
        404: {
            'description': 'Friend request not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        }
    }
})
def respond_friend(current_user):
     
    data = request.get_json()
    user_id =  data['response_user_id']
    if str(user_id) == str(g.user_id):
        return respond_friend_request(data)
    else:
        return jsonify({'message': 'Invalid request'}), 403
     
