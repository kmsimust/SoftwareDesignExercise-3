from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    # Login (POST)
    path("login/", views.user_login, name="user-login"),

    # List all users (GET) — supports ?name=
    path("", views.user_list, name="user-list"),

    # Get a single user (GET)
    path("<int:pk>/", views.user_detail, name="user-detail"),

    # Create a new user (POST)
    path("create/", views.user_create, name="user-create"),

    # Full update (PUT) or partial update (PATCH)
    path("<int:pk>/update/", views.user_update, name="user-update"),

    # Delete a user and their library (DELETE)
    path("<int:pk>/delete/", views.user_delete, name="user-delete"),
]