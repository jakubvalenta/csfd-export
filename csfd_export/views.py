import logging

from celery.result import AsyncResult
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django_ratelimit.decorators import ratelimit

from csfd_export.forms import UserForm
from csfd_export.scraper import ScraperError, UserNotFoundError
from csfd_export.tasks import scrape_user_ratings

logger = logging.getLogger(__name__)


@ratelimit(key="header:x-real-ip", rate="60/h", method=["POST"])
def index(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            uid = form.cleaned_data["uid"]
            result_id_cache_key = f"user:{uid}:result-id"
            if cache.get(result_id_cache_key) is None:
                # Run the task here, so that we can apply ratelimiting to scraping (POST view) while
                # not applying it to the checking of results (GET view).
                result = scrape_user_ratings.delay(uid)
                cache.set(result_id_cache_key, result.id, 3600)
            return redirect(reverse("user-detail", args=[uid]))
    else:
        form = UserForm()
    return render(request, "index.html", {"form": form})


def user_detail(request: HttpRequest, uid: int) -> HttpResponse:
    csv = ""
    error_message = ""
    status = 200
    result_id_cache_key = f"user:{uid}:result-id"
    result_id = cache.get(result_id_cache_key)
    if result_id is not None:
        result: AsyncResult = AsyncResult(result_id)
        if result.ready():
            try:
                csv = result.get()
            except ScraperError as e:
                error_message = e.args[0]
                status = 500
            except UserNotFoundError as e:
                error_message = e.args[0]
                status = 404
        else:
            result.forget()
            status = 201
    else:
        error_message = "Use the form please"
        status = 403
    if request.accepts("text/html"):
        return render(
            request,
            "users/detail.html",
            {
                "csv": csv,
                "error_message": error_message,
                "loading": status == 201,
                "uid": uid,
            },
            status=status,
        )
    return HttpResponse(
        error_message or csv,
        status=status,
        headers={"Content-Type": "text/csv"},
    )
