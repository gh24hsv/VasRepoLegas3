from models import db, User
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from config import Config

def register_user(data):
    # Check if user with the same email already exists
    existing_user = User.query.filter_by(user_email=data['user_email']).first()
    if existing_user:
        return jsonify({'message': 'Email already in use'}), 400
    
    # Create and add the new user if email is unique
    user = User(
        user_name=data['user_name'],
        user_email=data['user_email'],
        user_password=generate_password_hash(data['user_password']),
        user_type = "artist" if data['is_artist'] == True else "user"
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}),200

def login_user(data):
    user = User.query.filter_by(user_email=data['user_email']).first()
    if user and check_password_hash(user.user_password, data['user_password']):
        token = jwt.encode({
            'user_id': user.user_id,
            'user_type':user.user_type,            
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, Config.SECRET_KEY)
        return jsonify({'token': token}),200
    return jsonify({'message': 'Invalid credentials'}), 401
