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


def user_detail(request: HttpRequest, *, uid: int) -> HttpResponse:
    cache_key = f"user:{uid}:result-id"
    result_id = cache.get(cache_key)
    if result_id is None:
        result = scrape_user_ratings.delay(uid)
        result_id = result.id
        cache.set(cache_key, result_id, 30 * 3600)
    else:
        result = AsyncResult(result_id)
    if result.ready():
        csv_str = result.get()  # TODO Handle exceptions gracefully.
    else:
        result.forget()
        csv_str = None
    return render(request, "users/detail.html", {"csv": csv_str, "uid": uid})
