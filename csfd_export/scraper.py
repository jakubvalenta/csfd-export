import datetime
import logging
import re
import time
from dataclasses import dataclass
from typing import Iterable, Iterator

import requests
from bs4 import BeautifulSoup, NavigableString, Tag

logger = logging.getLogger(__name__)


class ParseError(Exception):
    pass


@dataclass
class Rating:
    title_cs: str
    year: int
    watched_datetime: datetime.datetime
    rating: float


def _http_get(url: str, timeout: int, user_agent: str) -> str:
    logger.info("Downloading %s", url)
    r = requests.get(
        url,
        headers={"User-Agent": user_agent},
        timeout=timeout,
    )
    r.raise_for_status()
    return r.text


def parse_last_page_num(soup: BeautifulSoup) -> int:
    page_links = soup.select(".box-user-rating .pagination a")
    page_num_links = [node for node in page_links if not node.get("class")]
    if len(page_num_links):
        last_page_num_link = page_num_links[-1]
        if last_page_num_link.string is None:
            raise ParseError("Failed to find last page number")
        last_page_num = int(last_page_num_link.string)
    else:
        last_page_num = 1
    logger.info("Found %d pages", last_page_num)
    return last_page_num


def _download_ratings_page(uid: int, page_no: int, **http_get_kwargs) -> str:
    return _http_get(
        f"https://www.csfd.cz/uzivatel/{uid}-uzivatel/hodnoceni/?page={page_no}",
        **http_get_kwargs,
    )


def download_ratings_pages(
    uid: int, *, interval: int, **http_get_kwargs
) -> Iterator[BeautifulSoup]:
    html = _download_ratings_page(uid, 1, **http_get_kwargs)
    first_page_soup = BeautifulSoup(html, "html.parser")
    yield first_page_soup
    last_page_num = parse_last_page_num(first_page_soup)
    for page_no in range(2, last_page_num + 1):
        logger.info("Waitig for %ds", interval)
        time.sleep(interval)
        html = _download_ratings_page(uid, page_no, **http_get_kwargs)
        yield BeautifulSoup(html, "html.parser")


def tag_or_none(val: Tag | NavigableString | None) -> Tag | None:
    if type(val) is Tag:
        return val
    return None


STAR_CLASS_REGEX = re.compile(r"stars-(?P<rating>\d)")


def parse_rating(star_classes: Iterable[str] | None) -> float:
    if star_classes:
        for star_class_ in star_classes:
            if star_class_ == "trash":
                return 0.5  # Use 0.5, because that's the lowest possible rating on Letterboxd.
            m = STAR_CLASS_REGEX.match(star_class_)
            if m:
                return int(m.group("rating"))
    raise ParseError("Failed to parse rating")


YEAR_REGEX = re.compile(r"\((?P<year>\d{4})\)")


def _parse_year(year_str: str | None) -> int:
    if year_str:
        m = YEAR_REGEX.search(year_str)
        if m:
            return int(m.group("year"))
    raise ParseError("Failed to parse year")


def _parse_watched_datetime(
    watched_datetime_strings: Iterable[str] | None,
) -> datetime.datetime:
    if watched_datetime_strings:
        for watched_datetime_str in watched_datetime_strings:
            try:
                return datetime.datetime.strptime(
                    watched_datetime_str.strip(), "%d.%m.%Y"
                )
            except ValueError:
                pass
    raise ParseError("Failed to parse watched date")


def parse_ratings_page(soup: BeautifulSoup) -> Iterator[Rating]:
    for tr in soup.select(".box-user-rating tr"):
        a_el = tag_or_none(tr.find(class_="film-title-name"))
        title_cs = a_el and a_el.string
        logger.info("Parsing %s", title_cs)
        if not title_cs:
            raise ParseError("Failed to parse film title")
        info_el = tag_or_none(tr.select_one(".film-title-info .info"))
        year = _parse_year(info_el.string if info_el else None)
        date_el = tag_or_none(tr.find(class_="date-only"))
        watched_datetime = _parse_watched_datetime(date_el.strings if date_el else None)
        stars_el = tag_or_none(tr.find(class_="stars"))
        rating = parse_rating(stars_el["class"] if stars_el else None)
        film = Rating(
            title_cs=title_cs,
            year=year,
            watched_datetime=watched_datetime,
            rating=rating,
        )
        yield film
