from django.urls import path

from . import views

app_name = "library"
 
urlpatterns = [
    # Get a user's library and all its songs (GET)
    path("<int:user_id>/", views.library_detail, name="library-detail"),
 
    # Create an empty library for a user (POST)
    path("<int:user_id>/create/", views.library_create, name="library-create"),
 
    # Add a song to the library (POST) — body: { "song_id": <int> }
    path("<int:user_id>/songs/add/", views.library_add_song, name="library-add-song"),
 
    # Remove a specific song from the library (DELETE)
    path("<int:user_id>/songs/<int:song_id>/remove/", views.library_remove_song, name="library-remove-song"),
 
    # Remove all songs from the library but keep the library (DELETE)
    path("<int:user_id>/clear/", views.library_clear, name="library-clear"),
 
    # Delete the library entirely (DELETE)
    path("<int:user_id>/delete/", views.library_delete, name="library-delete"),
]