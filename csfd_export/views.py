from celery.result import AsyncResult
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from csfd_export.forms import UserForm
from csfd_export.tasks import scrape_user_ratings


def index(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            return redirect(reverse("user-detail", args=[form.cleaned_data["uid"]]))
    else:
        form = UserForm()
    return render(request, "index.html", {"form": form})


def _get_user_detail_csv(uid: int) -> str | None:
    result_id_cache_key = f"user:{uid}:result-id"
    result_id = cache.get(result_id_cache_key)
    if result_id is None:
        # TODO Quickly check if the user exists.
        result = scrape_user_ratings.delay(uid)
        result_id = result.id
        cache.set(result_id_cache_key, result_id, 30 * 3600)
    else:
        result = AsyncResult(result_id)
    if result.ready():
        csv_str = result.get()  # TODO Handle exceptions gracefully.
    else:
        result.forget()
        csv_str = None
    return csv_str


def user_detail(request: HttpRequest, *, uid: int) -> HttpResponse:
    csv_str = _get_user_detail_csv(uid)
    return render(request, "users/detail.html", {"csv": csv_str, "uid": uid})


def api_user_detail(request: HttpRequest, *, uid: int) -> HttpResponse:
    csv_str = _get_user_detail_csv(uid)
    return HttpResponse(
        csv_str,
        status=200 if csv_str is not None else 404,
        headers={"Content-Type": "text/csv"},
    )
