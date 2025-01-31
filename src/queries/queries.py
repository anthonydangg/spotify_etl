def _get_song_insert_query():
    return '''
    INSERT INTO top_spotify.fact_rank(
        item_id,
        song_name,
        track_popularity,
        rank,
        created_at
    )
    VALUES (
        %(item_id)s,
        %(song_name)s,
        %(track_popularity)s,
        %(rank)s,
        %(created_at)s
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
    ) ON CONFLICT (artist_id) DO NOTHING;
    '''
