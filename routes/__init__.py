from .auth_routes import auth_bp
from .user_routes import user_bp
from .song_routes import song_bp
from .playlist_routes import playlist_bp
from .friend_routes import friend_bp
from .party_routes import party_bp

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(song_bp)
    app.register_blueprint(playlist_bp)
    app.register_blueprint(friend_bp)
    app.register_blueprint(party_bp)
