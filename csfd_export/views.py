import logging
from dataclasses import dataclass

from celery.result import AsyncResult
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from csfd_export.forms import UserForm
from csfd_export.scraper import ScraperError, UserNotFoundError
from csfd_export.tasks import scrape_user_ratings

logger = logging.getLogger(__name__)


@dataclass
class UserDetail:
    uid: int
    csv: str = ""
    error_message: str | None = None
    status: int = 200


def index(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            return redirect(reverse("user-detail", args=[form.cleaned_data["uid"]]))
    else:
        form = UserForm()
    return render(request, "index.html", {"form": form})


def _get_user_detail(uid: int) -> UserDetail:
    user_detail = UserDetail(uid)
    result_id_cache_key = f"user:{uid}:result-id"
    result_id = cache.get(result_id_cache_key)
    if result_id is None:
        result = scrape_user_ratings.delay(uid)
        result_id = result.id
        cache.set(result_id_cache_key, result_id, 3600)
    else:
        result = AsyncResult(result_id)
    if result.ready():
        try:
            user_detail.csv = result.get()
        except ScraperError as e:
            user_detail.error_message = e.args[0]
            user_detail.status = 500
        except UserNotFoundError as e:
            user_detail.error_message = e.args[0]
            user_detail.status = 404
    else:
        user_detail.status = 201
        result.forget()
    return user_detail


def user_detail(request: HttpRequest, *, uid: int) -> HttpResponse:
    user_detail = _get_user_detail(uid)
    logger.info(user_detail)
    return render(
        request,
        "users/detail.html",
        {
            "csv": user_detail.csv,
            "error_message": user_detail.error_message,
            "loading": user_detail.status == 201,
            "uid": user_detail.uid,
        },
        status=user_detail.status,
    )


def api_user_detail(request: HttpRequest, *, uid: int) -> HttpResponse:
    user_detail = _get_user_detail(uid)
    return HttpResponse(
        user_detail.error_message or user_detail.csv,
        status=user_detail.status,
        headers={"Content-Type": "text/csv"},
    )
