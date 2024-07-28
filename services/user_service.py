from models import db, User
from flask import jsonify

def get_user_profile(user_id):
    user = User.query.get(user_id)
    if user:
        user_data = {
            'user_id': user.user_id,
            'user_name': user.user_name,
            'user_email': user.user_email,
            'is_artist': user.is_artist,
            'created_at': user.created_at,
            'updated_at': user.updated_at,
            'is_active': user.is_active
        }
        return jsonify(user_data)
    return jsonify({'message': 'User not found'}), 404

def update_user_profile(user_id, data):
    user = User.query.get(user_id)
    if user:
        user.user_name = data.get('user_name', user.user_name)
        user.user_email = data.get('user_email', user.user_email)
        user.is_artist = data.get('is_artist', user.is_artist)
        user.updated_at = db.func.current_timestamp()
        db.session.commit()
        return jsonify({'message': 'User profile updated successfully'})
    return jsonify({'message': 'User not found'}), 404
