from functools import wraps
from flask import request, jsonify, g
import jwt
from config import Config
from models import User

def authorize(allowed_user_types):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None

            # Check if the token is provided in the Authorization header
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split(" ")[1]

            if not token:
                return jsonify({'message': 'Token is missing!'}), 401

            try:
                # Decode the token using the secret key
                data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
                current_user = User.query.get(data['user_id'])
                if not current_user:
                    return jsonify({'message': 'User not found!'}), 401

                # Check if the user's type is allowed
                if current_user.user_type not in allowed_user_types:
                    return jsonify({'message': 'Unauthorized user type!'}), 403

                # Set the user_id in a global variable to access in the app
                g.user_id = data['user_id']
                g.user_type = data['user_type']
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired!'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Invalid token!'}), 401

            return f(current_user, *args, **kwargs)

        return decorated_function
    return decorator
