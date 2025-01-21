CREATE SCHEMA top_spotify;

DROP TABLE IF EXISTS top_spotify.fact_rank;
DROP TABLE IF EXISTS top_spotify.track_artist;
DROP TABLE IF EXISTS top_spotify.artist;
DROP TABLE IF EXISTS top_spotify.artist_genres;

CREATE TABLE top_spotify.fact_rank
(
    item_id VARCHAR(50),
    song_name VARCHAR(50),
    track_popularity INT,
    rank INT
);

CREATE TABLE top_spotify.track_artist
(
    item_id VARCHAR(50),
    artist_id VARCHAR(50)
);

CREATE TABLE top_spotify.artist
(
    artist_id VARCHAR(50) UNIQUE,
    artist_name VARCHAR(50),
    artist_popularity INT
);

CREATE TABLE top_spotify.artist_genres
(
    artist_id VARCHAR(50) UNIQUE,
    genre VARCHAR(50)
);