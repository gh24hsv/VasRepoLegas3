from models import db, Friend
from flask import jsonify
import logging

logger = logging.getLogger(__name__)
# def send_friend_request(data):
#     friend = Friend(
#         request_user_id=data['request_user_id'],
#         response_user_id=data['response_user_id'],
#         status='pending',
#         created_by=data['request_user_id']
#     )
#     db.session.add(friend)
#     db.session.commit()
#     return jsonify({'message': 'Friend request sent successfully'})
def send_friend_request(data):
    try:
        # Create a new Friend object
        friend = Friend(
            request_user_id=data['request_user_id'],
            response_user_id=data['response_user_id'],
            status='pending',
            created_by=data['request_user_id']
        )
        
        # Add the Friend object to the session and commit
        db.session.add(friend)
        db.session.commit()
        
        # Log success message
        logger.info(f"Friend request sent successfully from {data['request_user_id']} to {data['response_user_id']}")
        return jsonify({'message': 'Friend request sent successfully'})
    
    except KeyError as e:
        # Handle missing keys in the data
        logger.error(f"Missing key in data: {e}")
        return jsonify({'message': 'Bad request, missing required fields'}), 400
    
    except Exception as e:
        # Handle any other exceptions
        logger.error(f"Error sending friend request: {e}")
        return jsonify({'message': 'Error sending friend request'}), 500

# def respond_friend_request(data):
#     friend = Friend.query.filter_by(request_user_id=data['request_user_id'], response_user_id=data['response_user_id']).first()
#     if friend:
#         friend.status = data['status']
#         friend.updated_at = db.func.current_timestamp()
#         db.session.commit()
#         return jsonify({'message': 'Friend request response updated successfully'})
#     return jsonify({'message': 'Friend request not found'}), 404

def respond_friend_request(data):
    try:
        # Retrieve the Friend object based on request_user_id and response_user_id
        friend = Friend.query.filter_by(request_user_id=data['request_user_id'], response_user_id=data['response_user_id']).first()
        
        if friend:
            # Update the Friend object's status and timestamp
            friend.status = data['status']
            friend.updated_at = db.func.current_timestamp()
            db.session.commit()
            
            # Log success message
            logger.info(f"Friend request response updated successfully for request_user_id {data['request_user_id']} and response_user_id {data['response_user_id']}")
            return jsonify({'message': 'Friend request response updated successfully'})
        
        # Log warning and return 404 if the friend request is not found
        logger.warning(f"Friend request not found for request_user_id {data['request_user_id']} and response_user_id {data['response_user_id']}")
        return jsonify({'message': 'Friend request not found'}), 404
    
    except KeyError as e:
        # Handle missing keys in the data
        logger.error(f"Missing key in data: {e}")
        return jsonify({'message': 'Bad request, missing required fields'}), 400
    
    except Exception as e:
        # Handle any other exceptions
        logger.error(f"Error responding to friend request: {e}")
        return jsonify({'message': 'Error responding to friend request'}), 500

# def get_friends_list(user_id):
#     friends = Friend.query.filter((Friend.request_user_id == user_id) | (Friend.response_user_id == user_id), Friend.status == 'accepted').all()
#     friend_list = []
#     for friend in friends:
#         friend_list.append({
#             'friend_id': friend.friend_id,
#             'request_user_id': friend.request_user_id,
#             'response_user_id': friend.response_user_id,
#             'status': friend.status,
#             'created_at': friend.created_at,
#             'updated_at': friend.updated_at,
#             'is_active': friend.is_active
#         })
#     return jsonify(friend_list)
def get_friends_list(user_id):
    try:
        # Query for friends with 'accepted' status
        friends = Friend.query.filter(
            (Friend.request_user_id == user_id) | (Friend.response_user_id == user_id),
            Friend.status == 'accepted'
        ).all()
        
        # Prepare the list of friends
        friend_list = []
        for friend in friends:
            friend_list.append({
                'friend_id': friend.friend_id,
                'request_user_id': friend.request_user_id,
                'response_user_id': friend.response_user_id,
                'status': friend.status,
                'created_at': friend.created_at,
                'updated_at': friend.updated_at,
                'is_active': friend.is_active
            })
        
        # Log success message
        logger.info(f"Retrieved friends list for user_id {user_id}")
        return jsonify(friend_list)
    
    except Exception as e:
        # Log the error and return a 500 response
        logger.error(f"Error retrieving friends list for user_id {user_id}: {e}")
        return jsonify({'message': 'Error retrieving friends list'}), 500