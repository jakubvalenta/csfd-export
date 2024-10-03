import csv
import io

from django.core.cache import caches
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from requests import HTTPError

from csfd_export.forms import UserForm
from csfd_export.scraper import download_ratings_pages, parse_ratings_page

cache = caches["default"]


def index(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            return redirect(reverse("user-detail", args=[form.cleaned_data["uid"]]))
    else:
        form = UserForm()
    return render(request, "index.html", {"form": form})


def user_detail(request: HttpRequest, *, uid: int) -> HttpResponse:
    cache_key = f"user:{uid}:csv"
    csv_str = cache.get(cache_key)
    if csv_str is None:
        ratings_pages = download_ratings_pages(
            uid,
            # TODO Move to interval, timeout and user_agent to settings.
            interval=2,
            timeout=10,
            user_agent="Mozilla/5.0 (Windows NT 10.0; rv:131.0) Gecko/20100101 Firefox/131.0",
        )
        f = io.StringIO()
        writer = csv.writer(f)
        writer.writerow(["Title", "Year", "Rating", "WatchedDate"])
        try:
            for soup in ratings_pages:
                for rating in parse_ratings_page(soup):
                    writer.writerow(
                        [
                            rating.title_cs,
                            rating.year,
                            rating.rating,
                            rating.watched_datetime.strftime("%Y-%m-%d"),
                        ]
                    )
        except HTTPError:
            raise Http404("ČSFD user not found")
        f.seek(0)
        csv_str = f.read()
        cache.set(cache_key, csv_str, 30 * 3600)
    return render(request, "users/detail.html", {"csv": csv_str, "uid": uid})
