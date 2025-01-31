import json
import os
from datetime import datetime

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from spotipy_anon import SpotifyAnon

from queries.queries import (
    _get_artist_genre_insert_query,
    _get_artist_insert_query,
    _get_song_insert_query,
    _get_track_artist_insert_query,
)
from utils.db import dbconnect


def get_spotify_client():
    sp = spotipy.Spotify(auth_manager=SpotifyAnon())

    return sp


def top_50_usa():
    sp = get_spotify_client()

    playlist_items = sp.playlist('37i9dQZEVXbLRQDuF5jeBp')['tracks']['items']

    data = []
    for item in playlist_items:
        data.append(
            {
                'item_id': item['track']['id'],
                'song_name': item['track']['name'],
                'artist_id': item['track']['artists'][0][
                    'id'
                ],
                'artist_name': item['track']['artists'][0]['name'],
                'genre': (
                    sp.artist(item['track']['artists'][0]['id'])['genres'][0]
                    if sp.artist(item['track']['artists'][0]['id'])['genres']
                    else None
                ),
                'track_popularity': item['track']['popularity'],
                'artist_popularity': sp.artist(
                    item['track']['artists'][0]['id']
                )['popularity'],
            }
        )

    data = json.dumps(data)
    return json.loads(data)


def insert():
    data = top_50_usa()
    with dbconnect() as cur:
        song_insert = _get_song_insert_query()
        track_artist_insert = _get_track_artist_insert_query()
        artist_insert = _get_artist_insert_query()
        artist_genre_insert = _get_artist_genre_insert_query()
        rank = 1
        for row in data:
            fact = {
                "item_id": row["item_id"],
                "song_name": row["song_name"],
                "track_popularity": row["track_popularity"],
                "rank": rank,
                "created_at": datetime.now()
            }
            rank += 1
            track_artist = {
                "item_id": row["item_id"],
                "artist_id": row["artist_id"],
            }
            artist = {
                "artist_id": row["artist_id"],
                "artist_name": row["artist_name"],
                "artist_popularity": row["artist_popularity"],
            }
            artist_genre = {
                "artist_id": row["artist_id"],
                "genre": row["genre"],
            }
            cur.execute(song_insert, fact)
            cur.execute(track_artist_insert, track_artist)
            cur.execute(artist_insert, artist)
            cur.execute(artist_genre_insert, artist_genre)


if __name__ == "__main__":
    insert()
