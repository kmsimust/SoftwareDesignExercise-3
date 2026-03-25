from django.urls import path
from . import views
 
app_name = "songs"
 
urlpatterns = [
    # List all songs (GET) — supports ?occasion= ?mood_tone= ?genre=
    path("", views.song_list, name="song-list"),
 
    # Get a single song (GET)
    path("<int:pk>/", views.song_detail, name="song-detail"),
 
    # Create a new song (POST)
    path("create/", views.song_create, name="song-create"),
 
    # Full update (PUT) or partial update (PATCH)
    path("<int:pk>/update/", views.song_update, name="song-update"),
 
    # Delete a song (DELETE)
    path("<int:pk>/delete/", views.song_delete, name="song-delete"),
]