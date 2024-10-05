import io

from django.conf import settings
from django.core.cache import caches
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from requests import HTTPError

from csfd_export.forms import UserForm
from csfd_export.scraper import download_ratings_pages, parse_ratings_pages, write_ratings_csv

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
        try:
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
            cache.set(cache_key, csv_str, 30 * 3600)
        except HTTPError:
            raise Http404("ČSFD user not found")
    return render(request, "users/detail.html", {"csv": csv_str, "uid": uid})
