# from flask import Blueprint, request, jsonify
# from services.song_service import get_all_songs, get_song, add_song, update_song

# song_bp = Blueprint('song', __name__)

# @song_bp.route('/songs', methods=['GET'])
# def songs():
#     return get_all_songs()

# @song_bp.route('/songs/<int:song_id>', methods=['GET'])
# def song(song_id):
#     return get_song(song_id)

# @song_bp.route('/songs', methods=['POST'])
# def add():
#     data = request.get_json()
#     return add_song(data)

# @song_bp.route('/songs/<int:song_id>', methods=['PUT'])
# def update(song_id):
#     data = request.get_json()
#     return update_song(song_id, data)

from flask import Flask, Blueprint, request, jsonify,send_from_directory
from services.song_service import get_all_songs, get_song, add_song, update_song,like_song,dislike_song
from flasgger import swag_from
from utils.helpers import authorize
import os
from flask import g
song_bp = Blueprint('song', __name__)
app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@song_bp.route('/songs', methods=['GET'])
@authorize(allowed_user_types=['user','artist'])
@swag_from({
    'tags': ['Songs'],
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'search',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Search term to filter songs by title'
        }
    ],
    'responses': {
        200: {
            'description': 'A list of songs',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'song_id': {'type': 'integer'},
                        'song_title': {'type': 'string'},
                        'artist_id': {'type': 'integer'},
                        'artist_name': {'type': 'string'},
                        'genre_id': {'type': 'integer'},
                        'genre_name': {'type': 'string'},
                        'language_id': {'type': 'integer'},
                        'language_name': {'type': 'string'},
                        'song_duration': {'type': 'integer'},
                        'song_lyrics': {'type': 'string'},
                        'song_source_url': {'type': 'string'},
                        'song_source_type': {'type': 'string'},
                        'created_at': {'type': 'string', 'format': 'date-time'},
                        'updated_at': {'type': 'string', 'format': 'date-time'},
                        'is_active': {'type': 'boolean'}
                    }
                }
            }
        }
    }
})
def songs(param):
    search = request.args.get('search')
    return get_all_songs(search_text=search)


@song_bp.route('/songs/<int:song_id>', methods=['GET'])
@authorize(allowed_user_types=['user', 'artist'])
@swag_from({
    'tags': ['Songs'],
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'song_id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'ID of the song to fetch'
        }
    ],
    'responses': {
        200: {
            'description': 'A single song',
            'schema': {
                'type': 'object',
                'properties': {
                    'song_id': {'type': 'integer'},
                    'song_title': {'type': 'string'},
                    'artist_id': {'type': 'integer'},
                    'artist_name': {'type': 'string'},
                    'genre_id': {'type': 'integer'},
                    'genre_name': {'type': 'string'},
                    'language_id': {'type': 'integer'},
                    'language_name': {'type': 'string'},
                    'song_duration': {'type': 'integer'},
                    'song_lyrics': {'type': 'string'},
                    'song_source_url': {'type': 'string'},
                    'song_source_type': {'type': 'string'},
                    'created_at': {'type': 'string', 'format': 'date-time'},
                    'updated_at': {'type': 'string', 'format': 'date-time'},
                    'is_active': {'type': 'boolean'}
                }
            }
        },
        404: {
            'description': 'Song not found'
        }
    }
})
def song(user_id,song_id):
    return get_song(song_id)


@song_bp.route('/songs', methods=['POST'])
@authorize(allowed_user_types=['artist'])
@swag_from({
    'tags': ['Songs'],
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'song_title': {'type': 'string', 'required': True},
                    'artist_id': {'type': 'integer', 'required': True},
                    'genre_id': {'type': 'integer', 'required': True},
                    'language_id': {'type': 'integer', 'required': True},
                    'song_duration': {'type': 'integer', 'required': True},
                    'song_lyrics': {'type': 'string'},
                    'song_source_url': {'type': 'string', 'required': True},
                    'song_source_type': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Song created successfully'
        },
        400: {
            'description': 'Invalid input'
        }
    }
})
def add():
    data = request.get_json()
    return add_song(data)

@song_bp.route('/songs/<int:song_id>', methods=['PUT'])
@authorize(allowed_user_types=['artist'])
@swag_from({
    'tags': ['Songs'],
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'song_title': {'type': 'string', 'required': True},
                    'artist_id': {'type': 'integer', 'required': True},
                    'genre_id': {'type': 'integer', 'required': True},
                    'language_id': {'type': 'integer', 'required': True},
                    'song_duration': {'type': 'integer', 'required': True},
                    'song_lyrics': {'type': 'string'},
                    'song_source_url': {'type': 'string', 'required': True},
                    'song_source_type': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Song updated successfully'
        },
        404: {
            'description': 'Song not found'
        }
    }
})
def update(song_id):
    data = request.get_json()
    return update_song(song_id, data)


@song_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@song_bp.route('/songs/<int:song_id>/like', methods=['POST'])
@authorize(allowed_user_types=['user', 'artist'])
@swag_from({
    'tags': ['Songs'],
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'song_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the song to like'
        }
    ],
    'responses': {
        200: {
            'description': 'Song liked successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        },
        400: {
            'description': 'Bad request',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        }
    }
})
def like(user_id,song_id):
    """Like a song"""
    return like_song(g.user_id, song_id)
     

@song_bp.route('/songs/<int:song_id>/dislike', methods=['POST'])
@authorize(allowed_user_types=['user', 'artist'])
@swag_from({
    'tags': ['Songs'],
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'song_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the song to dislike'
        }
    ],
    'responses': {
        200: {
            'description': 'Song disliked successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        },
        400: {
            'description': 'Bad request',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        }
    }
})
def dislike(user_id,song_id):
    """Dislike a song"""
    return dislike_song(g.user_id, song_id) 