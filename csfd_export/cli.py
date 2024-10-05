import argparse
import logging
import sys

from django.conf import settings

from csfd_export import __title__
from csfd_export.scraper import (
    download_ratings_pages, parse_ratings_pages, parse_uid, write_ratings_csv,
)

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(prog=__title__)
    parser.add_argument("profile_url", help="ČSFD profile URL")
    parser.add_argument(
        "output_csv",
        help="Output CSV file path",
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
        f"defaults to {settings.SCRAPER_INTERVAL}",
        type=int,
        default=settings.SCRAPER_INTERVAL,
    )
    parser.add_argument(
        "-t",
        "--timeout",
        help=f"HTTP request timeout in seconds; defaults to {settings.SCRAPER_TIMEOUT}",
        type=int,
        default=settings.SCRAPER_TIMEOUT,
    )
    parser.add_argument(
        "-u",
        "--user-agent",
        help=f"User-Agent header; defaults to {settings.SCRAPER_USER_AGENT}",
        default=settings.SCRAPER_USER_AGENT,
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
