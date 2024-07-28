# from models import db, Playlist, PlaylistSong
# from flask import jsonify

# def get_all_playlists():
#     playlists = Playlist.query.all()
#     playlist_list = []
#     for playlist in playlists:
#         playlist_list.append({
#             'playlist_id': playlist.playlist_id,
#             'user_id': playlist.user_id,
#             'playlist_name': playlist.playlist_name,
#             'thumbnail_url': playlist.thumbnail_url,
#             'is_private': playlist.is_private,
#             'created_at': playlist.created_at,
#             'updated_at': playlist.updated_at,
#             'is_active': playlist.is_active
#         })
#     return jsonify(playlist_list)

# def get_playlist(playlist_id):
#     playlist = Playlist.query.get(playlist_id)
#     if playlist:
#         playlist_data = {
#             'playlist_id': playlist.playlist_id,
#             'user_id': playlist.user_id,
#             'playlist_name': playlist.playlist_name,
#             'thumbnail_url': playlist.thumbnail_url,
#             'is_private': playlist.is_private,
#             'created_at': playlist.created_at,
#             'updated_at': playlist.updated_at,
#             'is_active': playlist.is_active
#         }
#         return jsonify(playlist_data)
#     return jsonify({'message': 'Playlist not found'}), 404

# def add_playlist(data):
#     playlist = Playlist(
#         user_id=data['user_id'],
#         playlist_name=data['playlist_name'],
#         thumbnail_url=data.get('thumbnail_url'),
#         is_private=data.get('is_private', False),
#         created_by=data['created_by']
#     )
#     db.session.add(playlist)
#     db.session.commit()
#     return jsonify({'message': 'Playlist added successfully'})

# def update_playlist(playlist_id, data):
#     playlist = Playlist.query.get(playlist_id)
#     if playlist:
#         playlist.playlist_name = data.get('playlist_name', playlist.playlist_name)
#         playlist.thumbnail_url = data.get('thumbnail_url', playlist.thumbnail_url)
#         playlist.is_private = data.get('is_private', playlist.is_private)
#         playlist.updated_at = db.func.current_timestamp()
#         db.session.commit()
#         return jsonify({'message': 'Playlist updated successfully'})
#     return jsonify({'message': 'Playlist not found'}), 404

from models import db, Playlist,Song,Genre,Artist,Language,Like,DisLike,PlaylistSong
from flask import jsonify,g

from sqlalchemy.orm import aliased
from sqlalchemy.sql import exists,case

def get_all_playlists(search_text=None):
    query = db.session.query(
        Playlist.playlist_id,
        Playlist.user_id,
        Playlist.playlist_name,
        Playlist.thumbnail_url,
        Playlist.is_private,
        Playlist.created_at,
        Playlist.updated_at,
        Playlist.is_active
    ).filter(Playlist.is_active == True)

    # Apply search filter if provided
    if search_text:
        query = query.filter(Playlist.playlist_name.ilike(f'%{search_text}%'))

    playlists = query.all()

    playlist_list = []
    for playlist in playlists:
        playlist_list.append({
            'playlist_id': playlist.playlist_id,
            'user_id': playlist.user_id,
            'playlist_name': playlist.playlist_name,
            'thumbnail_url': playlist.thumbnail_url,
            'is_private': playlist.is_private,
            'created_at': playlist.created_at.isoformat(),
            'updated_at': playlist.updated_at.isoformat(),
            'is_active': playlist.is_active
        })
    return jsonify(playlist_list)

# def get_playlist(playlist_id):
#     playlist = Playlist.query.get(playlist_id)
#     if playlist:
#         return jsonify({
#             'playlist_id': playlist.playlist_id,
#             'user_id': playlist.user_id,
#             'playlist_name': playlist.playlist_name,
#             'thumbnail_url': playlist.thumbnail_url,
#             'is_private': playlist.is_private,
#             'created_at': playlist.created_at.isoformat(),
#             'updated_at': playlist.updated_at.isoformat(),
#             'is_active': playlist.is_active
#         }), 200
#     return jsonify({'message': 'Playlist not found'}), 404

def get_playlist(playlist_id):
    # Fetch the playlist
    playlist = Playlist.query.get(playlist_id)
    
    if playlist:
        # Alias the tables for clarity in the join
        active_genres = aliased(Genre, Genre.query.filter(Genre.is_active == True).subquery())
        active_artists = aliased(Artist, Artist.query.filter(Artist.is_active == True).subquery())
        active_languages = aliased(Language, Language.query.filter(Language.is_active == True).subquery())
        
        # Subqueries to check user interactions
        user_id = g.get('user_id', None)  # Get the current user ID
        liked_subquery = db.session.query(Like.song_id).filter(Like.user_id == user_id).subquery()
        disliked_subquery = db.session.query(DisLike.song_id).filter(DisLike.user_id == user_id).subquery()

        # Query for songs in the playlist
        songs_query = db.session.query(
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
            Song.is_active == True,
            Song.song_id.in_(
                db.session.query(PlaylistSong.song_id).filter(PlaylistSong.playlist_id == playlist_id).subquery()
            )
        )

        # Fetch songs for the playlist
        songs = songs_query.all()
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

        # Return the playlist with the songs
        return jsonify({
            'playlist_id': playlist.playlist_id,
            'user_id': playlist.user_id,
            'playlist_name': playlist.playlist_name,
            'thumbnail_url': playlist.thumbnail_url,
            'is_private': playlist.is_private,
            'created_at': playlist.created_at.isoformat(),
            'updated_at': playlist.updated_at.isoformat(),
            'is_active': playlist.is_active,
            'songs': song_list
        }), 200
    
    return jsonify({'message': 'Playlist not found'}), 404

def add_playlist(data):
    playlist = Playlist(
        user_id=g.user_id,
        created_by=g.user_id,
        playlist_name=data['playlist_name'],
        thumbnail_url=data.get('thumbnail_url'),
        is_private=data.get('is_private', False)
    )
    db.session.add(playlist)
    db.session.commit()
    return jsonify({'message': 'Playlist added successfully'})

def update_playlist(playlist_id, data):
    playlist = Playlist.query.get(playlist_id)
    if playlist:
        playlist.playlist_name = data.get('playlist_name', playlist.playlist_name)
        playlist.thumbnail_url = data.get('thumbnail_url', playlist.thumbnail_url)
        playlist.is_private = data.get('is_private', playlist.is_private)
        playlist.updated_at = db.func.current_timestamp()
        db.session.commit()
        return jsonify({'message': 'Playlist updated successfully'})
    return jsonify({'message': 'Playlist not found'}), 404

def add_songs_to_playlist(playlist_id, data):
    # Fetch the playlist to ensure it exists
    playlist = Playlist.query.get(playlist_id)
    if not playlist:
        return jsonify({'message': 'Playlist not found'}), 404

    # Extract song IDs from the request data
    song_ids = data.get('song_ids', [])

    # Validate song IDs
    if not song_ids:
        return jsonify({'message': 'No song IDs provided'}), 400

    # Add songs to the playlist
    for song_id in song_ids:
        if not db.session.query(Song.query.filter_by(song_id=song_id).exists()).scalar():
            return jsonify({'message': f'Song with ID {song_id} not found'}), 404
        
        # Check if the song is already in the playlist
        if db.session.query(PlaylistSong.query.filter_by(playlist_id=playlist_id, song_id=song_id).exists()).scalar():
            continue
        
        # Add the song to the playlist
        playlist_song = PlaylistSong(playlist_id=playlist_id, song_id=song_id,order=1,created_by=g.user_id)
        db.session.add(playlist_song)

    # Commit the changes to the database
    db.session.commit()

    return jsonify({'message': 'Songs added to playlist successfully'}),200