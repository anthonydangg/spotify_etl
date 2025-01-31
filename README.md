# Spotify Charts Pipeline

Data pipeline that extracts the top songs from the Spotify API using Python, PostgresSQL, cron, Metabase, and Docker.

## Objective

The official Spotify Charts doesn't give you much information besides the ranking of certain songs. This project aims to give more insightful information about music trends through an interactive dashboard and by keeping track of the charts for longer periods of time. The pipeline calls the Spotify API every day at 3 pm (when Spotify updates their metrics) to extract the Spotify charts, load the data into a database, and apply transformations for visualizations in a dashboard. The project is hosted on AWS and the dashboard can be viewed here.

## Tools & Technologies

- Containerization - [**Docker**](https://www.docker.com), [**Docker Compose**](https://docs.docker.com/compose/)
- Database - [**PostgreSQL**](https://www.postgresql.org/)
- Data Visualization - [**Metabase**](https://www.metabase.com/)
- Language - [**Python**](https://www.python.org)

## Architecture

#### Pipeline
1. In `etl.py`, the data is pulled from the Spotify API, transformed, and inserted into a PostgreSQL database. 
2. The database connection setup is in `db.py`.
3. The data is separated into tables: fact_rank, track_artist, artist, and artist_genres.
4. The pipeline results are tested in `test_etl_integration.py` using pytest.
5. The above steps are containarized by Docker and deployed to an AWS EC2 instance.
