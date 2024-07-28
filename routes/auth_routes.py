from flask import Blueprint, request, jsonify
from services.auth_service import register_user, login_user
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        schema:
          id: Register
          required:
            - user_name
            - user_email
            - user_password
          properties:
            user_name:
              type: string
              description: The user's name
            user_email:
              type: string
              description: The user's email
            user_password:
              type: string
              description: The user's password
            is_artist:
              type: boolean
              description: The user's type. normal/artist
          required:
            - user_name
            - user_email
            - user_password
            - is_artist
    responses:
      201:
        description: User created successfully
      400:
        description: Invalid input
    """
    data = request.get_json()
    result = register_user(data)
    return result 

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        schema:
          id: Login
          required:
            - user_email
            - user_password
          properties:
            user_email:
              type: string
              description: The user's email
            user_password:
              type: string
              description: The user's password
    responses:
      200:
        description: Login successful
      401:
        description: Unauthorized
    """
    data = request.get_json()
    result = login_user(data)      
    return result 
