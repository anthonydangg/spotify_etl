from dotenv import load_dotenv
import os

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def get_spotify_client():
    load_dotenv('.env')
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    return spotipy.Spotify(auth_manager=auth_manager)

def get_top_50_tracks():
    sp = get_spotify_client()
    playlist_items = sp.playlist('37i9dQZEVXbLRQDuF5jeBp')['tracks']['items']

    for item in playlist_items:
        item_id = item['track']['id']
        song_name = item['track']['name']
        artist_id = item['track']['artists'][0]['id']
        artist_name = item['track']['artists'][0]['name']
        artist_genre = sp.artist(artist_id)['genres']
        track_popularity = item['track']['popularity']
        artist_popularity = sp.artist(artist_id)['popularity']
        print(item_id,song_name,artist_id,artist_name,artist_genre, track_popularity, artist_popularity)
        #just use dataframe then connect to db