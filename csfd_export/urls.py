from django.urls import path

from csfd_export import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "user/<int:uid>",
        views.user_detail,
        name="user-detail",
    ),
    path(
        "api/user/<int:uid>",
        views.api_user_detail,
        name="api-user-detail",
    ),
]
