from dotenv import load_dotenv
import os

import json

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from utils.db import dbconnect

def get_spotify_client():
    load_dotenv('.env')
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    return spotipy.Spotify(auth_manager=auth_manager)

def get_top_50_tracks():
    sp = get_spotify_client()
    playlist_items = sp.playlist('37i9dQZEVXbLRQDuF5jeBp')['tracks']['items']

    # data = []
    # for item in playlist_items:
    #     data.append({
    #         'item_id': item['track']['id'],
    #         'song_name': item['track']['name'],
    #         'artist_id': item['track']['artists'][0]['id'],
    #         'artist_name': item['track']['artists'][0]['name'],
    #         'artist_genre': sp.artist(item['track']['artists'][0]['id'])['genres'],
    #         'track_popularity': item['track']['popularity'],
    #         'artist_popularity': sp.artist(item['track']['artists'][0]['id'])['popularity']
    #     })

    # json_data = json.dumps(data)

    with dbconnect() as cur:
        insert = '''
                    INSERT INTO test(id)
                    VALUES (%s)'''
        value = (1,)
        cur.execute(insert, value)

get_top_50_tracks()

#insert Spotify API data into local postgres. proof of concept