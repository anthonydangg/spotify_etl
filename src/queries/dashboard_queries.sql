
-- Get current top 50
SELECT DISTINCT fact_rank.rank, fact_rank.song_name, artist.artist_name, fact_rank.track_popularity
FROM top_spotify.fact_rank
JOIN top_spotify.track_artist ON top_spotify.fact_rank.item_id = top_spotify.track_artist.item_id
JOIN top_spotify.artist ON track_artist.artist_id = artist.artist_id
WHERE fact_rank.created_at > CURRENT_DATE + TIME '15:00:00'
ORDER BY fact_rank.rank ASC

-- Get count of songs
SELECT COUNT(*)
FROM top_spotify.fact_rank
WHERE created_at > CURRENT_DATE + TIME '15:00:00'

-- Genre count
SELECT genre, COUNT(genre)
FROM top_spotify.artist_genres
GROUP BY artist_genres.genre
HAVING COUNT(genre) != 0

-- Artist popularity
SELECT artist_name as 'Artist', artist_popularity as 'Popularity'
FROM top_spotify.artist
ORDER BY artist_popularity DESC
LIMIT 10;

-- Artist appearance in top 50
SELECT artist_name as "Artist", COUNT(artist_name) as "Count"
FROM top_spotify.fact_rank
JOIN top_spotify.track_artist ON top_spotify.fact_rank.item_id = top_spotify.track_artist.item_id
JOIN top_spotify.artist ON track_artist.artist_id = artist.artist_id
GROUP BY artist_name
ORDER BY COUNT(artist_name) DESC
LIMIT 10;

-- Top 5 songs today over time
WITH top_5_songs_today AS (
    SELECT item_id, song_name
    FROM top_spotify.fact_rank
    WHERE fact_rank.created_at > CURRENT_DATE + TIME '15:00:00'
    ORDER BY rank ASC
    LIMIT 5
    )
    
SELECT 
    f.song_name,
    DATE(f.created_at) as date,
    AVG(f.track_popularity) as avg_popularity
FROM 
    top_spotify.fact_rank f
JOIN 
    top_5_songs_today t5 ON f.item_id = t5.item_id
GROUP BY 
    f.song_name, DATE(f.created_at)
ORDER BY 
    f.song_name, DATE(f.created_at);