from models import db, Song,Genre,Artist,Language,Like,DisLike
from flask import jsonify,request,g
from sqlalchemy.orm import aliased
from sqlalchemy.sql import exists,case
import logging
# def get_all_songs():
#     songs = Song.query.all()
#     song_list = []
#     for song in songs:
#         song_list.append({
#             'song_id': song.song_id,
#             'song_title': song.song_title,
#             'artist_id': song.artist_id,
#             'genre_id': song.genre_id,
#             'language_id': song.language_id,
#             'song_duration': song.song_duration,
#             'song_lyrics': song.song_lyrics,
#             'song_source_url': song.song_source_url,
#             'created_at': song.created_at,
#             'updated_at': song.updated_at,
#             'is_active': song.is_active
#         })
#     return jsonify(song_list)
logger = logging.getLogger(__name__)
def get_all_songs(search_text=None):

    user_id = g.get('user_id', None)  # Get the current user ID

    # Alias the tables for clarity in the join
    active_genres = aliased(Genre, Genre.query.filter(Genre.is_active == True).subquery())
    active_artists = aliased(Artist, Artist.query.filter(Artist.is_active == True).subquery())
    active_languages = aliased(Language, Language.query.filter(Language.is_active == True).subquery())
    # Subqueries to check user interactions
    liked_subquery = db.session.query(Like.song_id).filter(Like.user_id == user_id).subquery()
    disliked_subquery = db.session.query(DisLike.song_id).filter(DisLike.user_id == user_id).subquery()


    # Base query
    query = db.session.query(
        Song.song_id,
        Song.song_title,
        Song.artist_id,
        active_artists.artist_name,
        Song.genre_id,
        active_genres.genre_name,
        Song.language_id,
        active_languages.language_name,
        Song.song_duration,
        Song.song_lyrics,
        Song.song_source_url,
        Song.created_at,
        Song.updated_at,
        Song.is_active,
        exists().where(Song.song_id == liked_subquery.c.song_id).label('liked'),
        exists().where(Song.song_id == disliked_subquery.c.song_id).label('disliked')
    ).outerjoin(
        active_genres, Song.genre_id == active_genres.genre_id
    ).outerjoin(
        active_artists, Song.artist_id == active_artists.artist_id
    ).outerjoin(
        active_languages, Song.language_id == active_languages.language_id
    ).filter(
        Song.is_active == True
    )

    # Apply search filter if provided
    if search_text:
        query = query.filter(Song.song_title.ilike(f'%{search_text}%'))

    songs = query.all()

    song_list = []
    for song in songs:
        song_list.append({
            'song_id': song[0],
            'song_title': song[1],
            'artist_id': song[2],
            'artist_name': song[3] or '',
            'genre_id': song[4],
            'genre_name': song[5] or '',
            'language_id': song[6],
            'language_name': song[7] or '',
            'song_duration': song[8],
            'song_lyrics': song[9],
            'song_source_url': song[10],
            'created_at': song[11],
            'updated_at': song[12],
            'is_active': song[13],
            'liked': song[14],
            'disliked': song[15]
        })
    return jsonify(song_list)
def get_song(song_id):
    user_id = g.get('user_id',None)  # Get the current user ID

    # Alias the tables for clarity in the join
    active_genres = aliased(Genre, Genre.query.filter(Genre.is_active == True).subquery())
    active_artists = aliased(Artist, Artist.query.filter(Artist.is_active == True).subquery())
    active_languages = aliased(Language, Language.query.filter(Language.is_active == True).subquery())

    # Subqueries to check user interactions
    if user_id:
        liked_subquery = db.session.query(Like.song_id).filter(Like.user_id == user_id).subquery()
        disliked_subquery = db.session.query(DisLike.song_id).filter(DisLike.user_id == user_id).subquery()

        liked_expr = case(
            (exists().where(Song.song_id == liked_subquery.c.song_id), True),
            else_=False
        )
        disliked_expr = case(
            (exists().where(Song.song_id == disliked_subquery.c.song_id), True),
            else_=False
        )

        
    else:
        liked_expr = False
        disliked_expr = False

    # Base query
    query = db.session.query(
        Song.song_id,
        Song.song_title,
        Song.artist_id,
        active_artists.artist_name,
        Song.genre_id,
        active_genres.genre_name,
        Song.language_id,
        active_languages.language_name,
        Song.song_duration,
        Song.song_lyrics,
        Song.song_source_url,
        Song.created_at,
        Song.updated_at,
        Song.is_active,
        liked_expr.label('liked'),
        disliked_expr.label('disliked')
    ).outerjoin(
        active_genres, Song.genre_id == active_genres.genre_id
    ).outerjoin(
        active_artists, Song.artist_id == active_artists.artist_id
    ).outerjoin(
        active_languages, Song.language_id == active_languages.language_id
    ).filter(
        Song.is_active == True,
        Song.song_id == song_id  # Filter by song_id
    )

    # Fetch a single record
    song = query.first()

    if song:
        return jsonify({
            'song_id': song.song_id,
            'song_title': song.song_title,
            'artist_id': song.artist_id,
            'artist_name': song.artist_name or '',
            'genre_id': song.genre_id,
            'genre_name': song.genre_name or '',
            'language_id': song.language_id,
            'language_name': song.language_name or '',
            'song_duration': song.song_duration,
            'song_lyrics': song.song_lyrics,
            'song_source_url': song.song_source_url,
            'created_at': song.created_at.isoformat(),
            'updated_at': song.updated_at.isoformat(),
            'is_active': song.is_active,
            'liked': song.liked,
            'disliked': song.disliked
        }), 200
    else:
        return jsonify({'message': 'Song not found'}), 404

def add_song(data):
    song = Song(
        song_title=data['song_title'],
        artist_id=data['artist_id'],
        genre_id=data['genre_id'],
        language_id=data['language_id'],
        song_duration=data['song_duration'],
        song_lyrics=data.get('song_lyrics'),
        song_source_url=data['song_source_url'],
        created_by=data['created_by']
    )
    db.session.add(song)
    db.session.commit()
    return jsonify({'message': 'Song added successfully'})

def update_song(song_id, data):
    song = Song.query.get(song_id)
    if song:
        song.song_title = data.get('song_title', song.song_title)
        song.artist_id = data.get('artist_id', song.artist_id)
        song.genre_id = data.get('genre_id', song.genre_id)
        song.language_id = data.get('language_id', song.language_id)
        song.song_duration = data.get('song_duration', song.song_duration)
        song.song_lyrics = data.get('song_lyrics', song.song_lyrics)
        song.song_source_url = data.get('song_source_url', song.song_source_url)
        song.updated_at = db.func.current_timestamp()
        db.session.commit()
        return jsonify({'message': 'Song updated successfully'})
    return jsonify({'message': 'Song not found'}), 404


def like_song(user_id, song_id):
    # Check if the song has already been liked by the user
    existing_like = Like.query.filter_by(user_id=user_id, song_id=song_id).first()
    if existing_like:
        return {'message': 'Song already liked'}, 400

    # Remove any existing dislike (if any)
    DisLike.query.filter_by(user_id=user_id, song_id=song_id).delete()

    # Create a new like
    new_like = Like(user_id=user_id, song_id=song_id)
    db.session.add(new_like)
    db.session.commit()

    return {'message': 'Song liked successfully'}, 200

def dislike_song(user_id, song_id):
    # Check if the song has already been disliked by the user
    existing_dislike = DisLike.query.filter_by(user_id=user_id, song_id=song_id).first()
    if existing_dislike:
        return {'message': 'Song already disliked'}, 400

    # Remove any existing like (if any)
    Like.query.filter_by(user_id=user_id, song_id=song_id).delete()

    # Create a new dislike
    new_dislike = DisLike(user_id=user_id, song_id=song_id)
    db.session.add(new_dislike)
    db.session.commit()

    return {'message': 'Song disliked successfully'}, 200