from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    user_email = db.Column(db.String(100), unique=True, nullable=False)
    user_password = db.Column(db.String(255), nullable=False)
    is_artist = db.Column(db.Boolean, default=False)
    user_type = db.Column(db.String(20), default='normal') #artist admin
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    is_active = db.Column(db.Boolean, default=True)

class Artist(db.Model):
    __tablename__ = 'artists'

    artist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    artist_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    artist_name = db.Column(db.String(100), nullable=False)
    artist_bio = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    is_active = db.Column(db.Boolean, default=True)

class Genre(db.Model):
    __tablename__ = 'genres'

    genre_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    genre_name = db.Column(db.String(100), unique=True, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    is_active = db.Column(db.Boolean, default=True)

class Language(db.Model):
    __tablename__ = 'languages'

    language_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    language_name = db.Column(db.String(100), unique=True, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    is_active = db.Column(db.Boolean, default=True)

class Song(db.Model):
    __tablename__ = 'songs'

    song_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    song_title = db.Column(db.String(200), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.artist_id'))
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'))
    language_id = db.Column(db.Integer, db.ForeignKey('languages.language_id'))
    song_duration = db.Column(db.Integer, nullable=False)  # duration in seconds
    song_lyrics = db.Column(db.Text, nullable=True)
    song_lyrics_type = db.Column(db.String(30), default='text')  # api, url
    song_source_url = db.Column(db.String(2000), nullable=False)
    song_source_type = db.Column(db.String(30), nullable=True, default='local')  # api, online, etc
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    is_active = db.Column(db.Boolean, default=True)

class Tag(db.Model):
    __tablename__ = 'tags'

    tag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_name = db.Column(db.String(100), unique=True, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    is_active = db.Column(db.Boolean, default=True)

class SongTag(db.Model):
    __tablename__ = 'song_tags'

    song_tag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.song_id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    is_active = db.Column(db.Boolean, default=True)

class Like(db.Model):
    __tablename__ = 'likes'

    like_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    song_id = db.Column(db.Integer, db.ForeignKey('songs.song_id')) 
    liked_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class DisLike(db.Model):
    __tablename__ = 'dislikes'

    dislike_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    song_id = db.Column(db.Integer, db.ForeignKey('songs.song_id')) 
    disliked_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Playlist(db.Model):
    __tablename__ = 'playlists'

    playlist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    playlist_name = db.Column(db.String(100), nullable=False)
    thumbnail_url = db.Column(db.String(255))
    is_private = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    is_active = db.Column(db.Boolean, default=True)

class PlaylistSong(db.Model):
    __tablename__ = 'playlist_songs'

    playlist_song_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.playlist_id'))
    song_id = db.Column(db.Integer, db.ForeignKey('songs.song_id'))
    order = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    is_active = db.Column(db.Boolean, default=True)

class Friend(db.Model):
    __tablename__ = 'friends'

    friend_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    response_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    status = db.Column(db.String(20), default='pending')  # pending, accepted, declined
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    is_active = db.Column(db.Boolean, default=True)

class Party(db.Model):
    __tablename__ = 'parties'

    party_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    party_name = db.Column(db.String(100), nullable=False)
    party_host_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    is_active = db.Column(db.Boolean, default=True)

class PartyMember(db.Model):
    __tablename__ = 'party_members'

    party_member_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    member_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    party_id = db.Column(db.Integer, db.ForeignKey('parties.party_id'))
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    is_active = db.Column(db.Boolean, default=True)

class PartyPlaylistSong(db.Model):
    __tablename__ = 'party_playlist_songs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    party_id = db.Column(db.Integer, db.ForeignKey('parties.party_id'))
    song_id = db.Column(db.Integer, db.ForeignKey('songs.song_id'))
    order = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    is_active = db.Column(db.Boolean, default=True)

class PlaybackHistory(db.Model):
    __tablename__ = 'playback_histories'

    playback_history_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    song_id = db.Column(db.Integer, db.ForeignKey('songs.song_id'))
    is_live = db.Column(db.Boolean, default=True)
    device_info = db.Column(db.String(1000))
    played_at = db.Column(db.DateTime, default=db.func.current_timestamp())
