from models import db, Party, PartyPlaylistSong
from flask import jsonify

def create_party(data):
    party = Party(
        party_name=data['party_name'],
        party_host_id=data['party_host_id'],
        created_by=data['created_by']
    )
    db.session.add(party)
    db.session.commit()
    return jsonify({'message': 'Party created successfully'})

def add_song_to_party(party_id, data):
    party_song = PartyPlaylistSong(
        party_id=party_id,
        song_id=data['song_id'],
        order=data['order'],
        created_by=data['created_by']
    )
    db.session.add(party_song)
    db.session.commit()
    return jsonify({'message': 'Song added to party playlist successfully'})

def get_party_playlist(party_id):
    party_songs = PartyPlaylistSong.query.filter_by(party_id=party_id).all()
    party_song_list = []
    for party_song in party_songs:
        party_song_list.append({
            'id': party_song.id,
            'party_id': party_song.party_id,
            'song_id': party_song.song_id,
            'order': party_song.order,
            'created_at': party_song.created_at,
            'updated_at': party_song.updated_at,
            'is_active': party_song.is_active
        })
    return jsonify(party_song_list)
