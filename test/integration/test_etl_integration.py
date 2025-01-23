import pytest
import csv

from etl import insert
from utils.db import dbconnect

class TestETLIntegration:
    def teardown_method(self):
        with dbconnect() as cur:
            cur.execute("TRUNCATE TABLE top_spotify.fact_rank;")
            #have to truncate all tables

    def get_table_data(self):
        with dbconnect() as cur:
            cur.execute("SELECT * FROM top_spotify.fact_rank;")
            data = cur.fetchall()
        return data

    def test_etl_fact(self, mocker):
        with open('test/fixture/top50_fixture.csv') as f:
            mock_data = [row for row in csv.DictReader(f)]
        
        mocker.patch('etl.top_50_usa', return_value=mock_data)
        insert()
        expected_fact = [ #turn to tuples instead
            {
                "item_id": "3sK8wGT43QFpWrvNQsrQya",
                "song_name": "DtMF",
                "track_popularity": 96,
                "rank": 1
            },
            {
                "item_id": "2plbrEY59IikOBgBGLjaoe",
                "song_name": "Die With A Smile",
                "track_popularity": 96,
                "rank": 2
            },
            {
                "item_id": "2CGNAOSuO1MEFCbBRgUzjd",
                "song_name": "luther (with sza)",
                "track_popularity": 87,
                "rank": 3
            },
            {
                "item_id": "2lTm559tuIvatlT1u0JYG2",
                "song_name": "BAILE INoLVIDABLE",
                "track_popularity": 94,
                "rank": 4
            },
            {
                "item_id": "0aB0v4027ukVziUGwVGYpG",
                "song_name": "tv off (feat. lefty gunplay)",
                "track_popularity": 91,
                "rank": 5
            },
        ]
        actual = self.get_table_data()
        assert expected_fact == actual