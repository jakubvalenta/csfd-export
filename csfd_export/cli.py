import argparse
import logging
import sys

from csfd_export import __title__
from csfd_export.scraper import (
    DEFAULT_INTERVAL, DEFAULT_TIMEOUT, DEFAULT_USER_AGENT, download_ratings_pages,
    parse_ratings_pages, parse_uid, write_ratings_csv,
)

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(prog=__title__)
    parser.add_argument(
        "profile_url",
        help="ČSFD profile URL; example: https://www.csfd.cz/uzivatel/18708-polaroid/hodnoceni/",
    )
    parser.add_argument(
        "output_csv",
        help="Output CSV file path; defaults to - which means standard output",
        nargs="?",
        type=argparse.FileType("w"),
        default=sys.stdout,
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable debugging output"
    )
    parser.add_argument(
        "-i",
        "--interval",
        help="Number of seconds to wait between HTTP requests; "
        f"defaults to {DEFAULT_INTERVAL}",
        type=int,
        default=DEFAULT_INTERVAL,
    )
    parser.add_argument(
        "-t",
        "--timeout",
        help=f"HTTP request timeout in seconds; defaults to {DEFAULT_TIMEOUT}",
        type=int,
        default=DEFAULT_TIMEOUT,
    )
    parser.add_argument(
        "-u",
        "--user-agent",
        help=f"User-Agent header; defaults to {DEFAULT_USER_AGENT}",
        default=DEFAULT_USER_AGENT,
    )
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="%(message)s")

    uid = parse_uid(args.profile_url)
    ratings_pages = download_ratings_pages(
        uid, interval=args.interval, timeout=args.timeout, user_agent=args.user_agent
    )
    ratings = parse_ratings_pages(ratings_pages)
    write_ratings_csv(ratings, args.output_csv)


if __name__ == "__main__":
    main()
