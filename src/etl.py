from dotenv import load_dotenv
import os

import json

import spotipy
from spotipy_anon import SpotifyAnon
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth


from utils.db import dbconnect

def get_spotify_client():
    load_dotenv('.env')
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    
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
            'artist_genre': sp.artist(item['track']['artists'][0]['id'])['genres'],
            'track_popularity': item['track']['popularity'],
            'artist_popularity': sp.artist(item['track']['artists'][0]['id'])['popularity']
        })

    json_data = json.dumps(data)

def _get_song_insert_query():
    return '''
    INSERT INTO top_spotify.fact_rank(
        item_id,
        song_name,
        track_popularity
    )
    VALUES (
        %(item_id)s,
        %(song_name)s,
        %(track_popularity)s
    );
    '''

# def insert():
#     with dbconnect() as cur:
#         insert = '''
#                     INSERT INTO test(id)
#                     VALUES (%s)'''
#         value = (2,)
#         cur.execute(insert, value)

top_50_usa()