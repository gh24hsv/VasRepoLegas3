from flask import Blueprint, request, jsonify
from services.user_service import get_user_profile, update_user_profile

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile/<int:user_id>', methods=['GET'])
def profile(user_id):
    return get_user_profile(user_id)

@user_bp.route('/profile/<int:user_id>', methods=['PUT'])
def update_profile(user_id):
    data = request.get_json()
    return update_user_profile(user_id, data)
