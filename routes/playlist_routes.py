# from flask import Blueprint, request, jsonify
# from services.playlist_service import get_all_playlists, get_playlist, add_playlist, update_playlist

# playlist_bp = Blueprint('playlist', __name__)

# @playlist_bp.route('/playlists', methods=['GET'])
# def playlists():
#     return get_all_playlists()

# @playlist_bp.route('/playlists/<int:playlist_id>', methods=['GET'])
# def playlist(playlist_id):
#     return get_playlist(playlist_id)

# @playlist_bp.route('/playlists', methods=['POST'])
# def add():
#     data = request.get_json()
#     return add_playlist(data)

# @playlist_bp.route('/playlists/<int:playlist_id>', methods=['PUT'])
# def update(playlist_id):
#     data = request.get_json()
#     return update_playlist(playlist_id, data)
from flask import Blueprint, request, jsonify
from services.playlist_service import get_all_playlists, get_playlist, add_playlist, update_playlist,add_songs_to_playlist
from flasgger import swag_from
from utils.helpers import authorize

playlist_bp = Blueprint('playlist', __name__)

@playlist_bp.route('/playlists', methods=['GET'])
@authorize(allowed_user_types=['user', 'artist'])
@swag_from({
    'tags': ['Playlists'],
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'search',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Search term to filter playlists by name'
        }
    ],
    'responses': {
        200: {
            'description': 'A list of playlists',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'playlist_id': {'type': 'integer'},
                        'user_id': {'type': 'integer'},
                        'playlist_name': {'type': 'string'},
                        'thumbnail_url': {'type': 'string'},
                        'is_private': {'type': 'boolean'},
                        'created_at': {'type': 'string', 'format': 'date-time'},
                        'updated_at': {'type': 'string', 'format': 'date-time'},
                        'is_active': {'type': 'boolean'}
                    }
                }
            }
        }
    }
})
def playlists(user_id):
    search = request.args.get('search')
    return get_all_playlists(search_text=search)

@playlist_bp.route('/playlists/<int:playlist_id>', methods=['GET'])
@authorize(allowed_user_types=['user', 'artist'])
@swag_from({
    'tags': ['Playlists'],
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'playlist_id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'ID of the playlist to fetch'
        }
    ],
    'responses': {
        200: {
            'description': 'A single playlist',
            'schema': {
                'type': 'object',
                'properties': {
                    'playlist_id': {'type': 'integer'},
                    'user_id': {'type': 'integer'},
                    'playlist_name': {'type': 'string'},
                    'thumbnail_url': {'type': 'string'},
                    'is_private': {'type': 'boolean'},
                    'created_at': {'type': 'string', 'format': 'date-time'},
                    'updated_at': {'type': 'string', 'format': 'date-time'},
                    'is_active': {'type': 'boolean'}
                }
            }
        },
        404: {
            'description': 'Playlist not found'
        }
    }
})
def playlist(user_id,playlist_id):
    return get_playlist(playlist_id)

@playlist_bp.route('/playlists', methods=['POST'])
@authorize(allowed_user_types=['user', 'artist'])
@swag_from({
    'tags': ['Playlists'],
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'playlist_name': {'type': 'string', 'required': True},
                    'thumbnail_url': {'type': 'string'},
                    'is_private': {'type': 'boolean'},
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Playlist created successfully'
        },
        400: {
            'description': 'Invalid input'
        }
    }
})
def add(user_id):
    data = request.get_json()
    return add_playlist(data)

@playlist_bp.route('/playlists/<int:playlist_id>', methods=['PUT'])
@authorize(allowed_user_types=['user', 'artist'])
@swag_from({
    'tags': ['Playlists'],
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'playlist_name': {'type': 'string'},
                    'thumbnail_url': {'type': 'string'},
                    'is_private': {'type': 'boolean'},
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Playlist updated successfully'
        },
        404: {
            'description': 'Playlist not found'
        }
    }
})
def update(user_id,playlist_id):
    data = request.get_json()
    return update_playlist(playlist_id, data)

@playlist_bp.route('/playlists/<int:playlist_id>/songs', methods=['POST'])
@authorize(allowed_user_types=['artist','user'])
@swag_from({
    'tags': ['Playlists'],
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'playlist_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the playlist to add songs to'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'song_ids': {
                        'type': 'array',
                        'items': {'type': 'integer'},
                        'description': 'List of song IDs to add to the playlist'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Songs added to playlist successfully'
        },
        404: {
            'description': 'Playlist not found'
        }
    }
})
def add_songs(user_id,playlist_id):
    data = request.get_json()
    return add_songs_to_playlist(playlist_id, data)
