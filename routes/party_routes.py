from flask import Blueprint, request, jsonify
from services.party_service import create_party, add_song_to_party, get_party_playlist

party_bp = Blueprint('party', __name__)

@party_bp.route('/parties', methods=['POST'])
def create():
    data = request.get_json()
    return create_party(data)

@party_bp.route('/parties/<int:party_id>/songs', methods=['POST'])
def add_song(party_id):
    data = request.get_json()
    return add_song_to_party(party_id, data)

@party_bp.route('/parties/<int:party_id>/playlist', methods=['GET'])
def playlist(party_id):
    return get_party_playlist(party_id)
