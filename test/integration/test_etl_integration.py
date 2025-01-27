import csv

import pytest

from etl import insert
from utils.db import dbconnect


class TestETLIntegration:
    def teardown_method(self):
        with dbconnect() as cur:
            cur.execute("TRUNCATE TABLE top_spotify.fact_rank;")
            cur.execute("TRUNCATE TABLE top_spotify.track_artist;")
            cur.execute("TRUNCATE TABLE top_spotify.artist;")
            cur.execute("TRUNCATE TABLE top_spotify.artist_genres;")

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

        expected_fact = [
            ('3sK8wGT43QFpWrvNQsrQya', 'DtMF', 96, 1),
            ("2plbrEY59IikOBgBGLjaoe", "Die With A Smile", 100, 2),
            ("2CGNAOSuO1MEFCbBRgUzjd", "luther (with sza)", 87, 3),
            ("2lTm559tuIvatlT1u0JYG2", "BAILE INoLVIDABLE", 94, 4),
            ("0aB0v4027ukVziUGwVGYpG", "tv off (feat. lefty gunplay)", 91, 5),
        ]

        actual = self.get_table_data()
        assert expected_fact == actual
