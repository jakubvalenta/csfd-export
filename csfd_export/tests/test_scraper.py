import datetime
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from csfd_export.scraper import (
    Rating, ScraperError, parse_last_page_num, parse_rating, parse_ratings_page, parse_uid,
)

hodnoceni_soup = BeautifulSoup(
    (Path(__file__).parent / "test_data" / "hodnoceni.html").read_text(),
    "html.parser",
)
ratings_soup = BeautifulSoup(
    (Path(__file__).parent / "test_data" / "ratings.html").read_text(),
    "html.parser",
)


def test_parse_uid():
    assert parse_uid("https://www.csfd.sk/uzivatel/18708-polaroid/hodnotenia/") == 18708
    assert (
        parse_uid("https://www.filmbooster.co.uk/user/18708-polaroid/ratings/") == 18708
    )
    assert (
        parse_uid("https://www.filmbooster.com.au/user/18708-polaroid/ratings/")
        == 18708
    )
    assert (
        parse_uid("https://www.filmbooster.de/nutzer/18708-polaroid/bewertungen/")
        == 18708
    )
    assert parse_uid("https://www.csfd.cz/uzivatel/18708-polaroid") == 18708
    assert parse_uid("https://www.csfd.cz/uzivatel/18708-polaroid/") == 18708
    assert parse_uid("https://www.csfd.cz/uzivatel/18708-polaroid/prehled/") == 18708
    assert parse_uid("https://www.csfd.cz/uzivatel/18708-polaroid/hodnoceni/") == 18708
    assert parse_uid("https://www.csfd.cz/uzivatel/18708-polaroid/spam/") == 18708
    assert parse_uid("https://www.csfd.cz/uzivatel/18708-polaroid/foo/bar/") == 18708
    assert parse_uid("https://www.csfd.cz/uzivatel/00123-+ěčř/foo/bar/") == 123
    assert parse_uid("https://csfd.cz/uzivatel/18708-polaroid") == 18708
    assert parse_uid("http://csfd.cz/uzivatel/18708-polaroid") == 18708
    assert parse_uid("csfd.cz/uzivatel/18708-polaroid") == 18708
    with pytest.raises(ScraperError):
        parse_uid("18708-polaroid")
    with pytest.raises(ScraperError):
        parse_uid("uzivatel/18708-polaroid")
    with pytest.raises(ScraperError):
        parse_uid("https://www.csfd.cz/uzivatel/00123foo/foo/bar/")
    with pytest.raises(ScraperError):
        parse_uid("https://www.example.com/")


def test_parse_star_classes():
    assert parse_rating(["star", "stars-5"]) == 5
    assert parse_rating(["star", "stars-1"]) == 1
    assert parse_rating(["star", "trash"]) == 0.5
    with pytest.raises(ScraperError):
        parse_rating([])
    with pytest.raises(ScraperError):
        parse_rating(["stars-x"])


def test_parse_ratings_page():
    films = list(parse_ratings_page(hodnoceni_soup))
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


def test_parse_ratings_page_english():
    films = list(parse_ratings_page(ratings_soup))
    assert films[0] == Rating(
        title_cs="Game of Thrones",
        year=2011,
        watched_datetime=datetime.datetime(2012, 3, 23),
        rating=3,
    )
    assert films[16] == Rating(
        title_cs="Brüno",
        year=2009,
        watched_datetime=datetime.datetime(2011, 12, 10),
        rating=0.5,
    )
    assert films[-1] == Rating(
        title_cs="Justice : Stress",
        year=2008,
        watched_datetime=datetime.datetime(2010, 11, 28),
        rating=1,
    )


def test_parse_last_page_num():
    assert parse_last_page_num(hodnoceni_soup) == 24
    assert parse_last_page_num(ratings_soup) == 27
