import datetime
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from csfd_export.scraper import (
    ParseError, Rating, parse_last_page_num, parse_rating, parse_ratings_page,
)

soup_profile = BeautifulSoup(
    (Path(__file__).parent / "test_data" / "hodnoceni.html").read_text(),
    "html.parser",
)


def test_parse_star_classes():
    assert parse_rating(["star", "stars-5"]) == 5
    assert parse_rating(["star", "stars-1"]) == 1
    assert parse_rating(["star", "trash"]) == 0.5
    with pytest.raises(ParseError):
        parse_rating([])
    with pytest.raises(ParseError):
        parse_rating(["stars-x"])


def test_parse_ratings_page():
    films = list(parse_ratings_page(soup_profile))
    assert films[0] == Rating(
        title_cs="The Matrix Resurrections",
        year=2021,
        watched_datetime=datetime.datetime(2021, 12, 29),
        rating=2,
    )
    assert films[32] == Rating(
        title_cs="The Power of Nightmares",
        year=2004,
        watched_datetime=datetime.datetime(2021, 4, 24),
        rating=5,
    )
    assert films[-1] == Rating(
        title_cs="Tenkrát v Hollywoodu",
        year=2019,
        watched_datetime=datetime.datetime(2021, 1, 30),
        rating=0.5,
    )


def test_parse_last_page_num():
    assert parse_last_page_num(soup_profile) == 24
