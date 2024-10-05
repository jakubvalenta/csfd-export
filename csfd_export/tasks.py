import io

from celery import Celery
from django.conf import settings

from csfd_export.scraper import download_ratings_pages, parse_ratings_pages, write_ratings_csv

app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER,
    backend=settings.CELERY_BACKEND,
    broker_connection_retry_on_startup=True,
)


@app.task
def scrape_user_ratings(uid: int) -> str:
    ratings_pages = download_ratings_pages(
        uid,
        interval=settings.SCRAPER_INTERVAL,
        timeout=settings.SCRAPER_TIMEOUT,
        user_agent=settings.SCRAPER_USER_AGENT,
    )
    ratings = parse_ratings_pages(ratings_pages)
    f = io.StringIO()
    write_ratings_csv(ratings, f)
    f.seek(0)
    csv_str = f.read()
    return csv_str
