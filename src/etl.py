import os

import json

import spotipy
from spotipy_anon import SpotifyAnon
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth


from utils.db import dbconnect

def get_spotify_client():
    sp = spotipy.Spotify(auth_manager=SpotifyAnon())

    return sp

def top_50_usa():
    sp = get_spotify_client()

    playlist_items = sp.playlist('37i9dQZEVXbLRQDuF5jeBp')['tracks']['items']

    data = []
    for item in playlist_items:
        data.append({
            'item_id': item['track']['id'],
            'song_name': item['track']['name'],
            'artist_id': item['track']['artists'][0]['id'], #only takes the first artist. should account for features later
            'artist_name': item['track']['artists'][0]['name'],
            'genre': sp.artist(item['track']['artists'][0]['id'])['genres'],
            'track_popularity': item['track']['popularity'],
            'artist_popularity': sp.artist(item['track']['artists'][0]['id'])['popularity']
        })

    data = json.dumps(data)
    return json.loads(data)

def _get_song_insert_query():
    return '''
    INSERT INTO top_spotify.fact_rank(
        item_id,
        song_name,
        artist_id,
        track_popularity
    )
    VALUES (
        %(item_id)s,
        %(song_name)s,
        %(artist_id)s,
        %(track_popularity)s
    );
    '''

def _get_track_artist_insert_query():
    return '''
    INSERT INTO top_spotify.track_artist(
        item_id,
        artist_id
    )
    VALUES (
        %(item_id)s,
        %(artist_id)s
    );
    '''

def _get_artist_insert_query():
    return '''
    INSERT INTO top_spotify.artist(
        artist_id,
        artist_name,
        artist_popularity
    )
    VALUES (
        %(artist_id)s,
        %(artist_name)s,
        %(artist_popularity)s
    ) ON CONFLICT (artist_id) DO NOTHING;
    '''

def _get_artist_genre_insert_query():
    return '''
    INSERT INTO top_spotify.artist_genres(
        artist_id,
        genre
    )
    VALUES (
        %(artist_id)s,
        %(genre)s
    );
    '''

def insert():
    data = top_50_usa()
    print(data)
    with dbconnect() as cur:
        song_insert = _get_song_insert_query()
        track_artist_insert = _get_track_artist_insert_query()
        artist_insert = _get_artist_insert_query()
        artist_genre_insert = _get_artist_genre_insert_query()
        for row in data:
            fact = {
                "item_id": row["item_id"],
                "song_name": row["song_name"],
                "track_popularity": row["track_popularity"]
                #add rank 
            }
            track_artist = {
                "item_id": row["item_id"],
                "artist_id": row["artist_id"]
                #add dup artist cause multiple track of same artist
            }
            artist = {
                "artist_id": row["artist_id"],
                "artist_name": row["artist_name"],
                "artist_popularity": row["artist_popularity"]
            }
            artist_genre = {
                "artist_id": row["artist_id"],
                "genre": row["genre"]
                #have to fix by iterating through the list of genres
            }
            cur.execute(song_insert, fact)
            cur.execute(track_artist_insert, track_artist)
            cur.execute(artist_insert, artist)
            # cur.execute(artist_genre_insert, artist_genre)

insert()
