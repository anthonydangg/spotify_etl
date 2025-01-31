
-- Get current top 50
SELECT DISTINCT fact_rank.rank, fact_rank.song_name, artist.artist_name, fact_rank.track_popularity
FROM top_spotify.fact_rank
JOIN top_spotify.track_artist ON top_spotify.fact_rank.item_id = top_spotify.track_artist.item_id
JOIN top_spotify.artist ON track_artist.artist_id = artist.artist_id
WHERE fact_rank.created_at > CURRENT_DATE + TIME '23:00:00' - interval '1 day'
ORDER BY fact_rank.rank ASC

-- add where statement for today.