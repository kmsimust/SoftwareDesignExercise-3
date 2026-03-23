from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User, Library, Song


def _serialize_song(song):
    return {
        "id":             song.pk,
        "title":          song.title,
        "occasion":       song.occasion,
        "mood_tone":      song.mood_tone,
        "genre":          song.genre,
        "singer_voice":   song.singer_voice,
        "meaning":        song.meaning,
        "song_durations": str(song.song_durations),
    }

def _serialize_library(library):
    return {
        "id":    library.pk,
        "user":  {
            "id":    library.user.pk,
            "name":  library.user.name,
            "email": library.user.email,
        },
        "songs":       [_serialize_song(s) for s in library.songs.all()],
        "total_songs": library.songs.count(),
    }


@require_http_methods(["GET"])
def library_detail(request, user_id):
    user    = get_object_or_404(User, pk=user_id)
    library = get_object_or_404(Library, user=user)
    return JsonResponse(_serialize_library(library), status=200)


@csrf_exempt
@require_http_methods(["POST"])
def library_create(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if Library.objects.filter(user=user).exists():
        return JsonResponse(
            {"error": f"User '{user.name}' already has a library."},
            status=400,
        )

    library = Library.objects.create(user=user)
    return JsonResponse(_serialize_library(library), status=201)


@csrf_exempt
@require_http_methods(["POST"])
def library_add_song(request, user_id):
    user    = get_object_or_404(User, pk=user_id)
    library = get_object_or_404(Library, user=user)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body."}, status=400)

    song_id = body.get("song_id")
    if not song_id:
        return JsonResponse({"error": "song_id is required."}, status=400)

    song = get_object_or_404(Song, pk=song_id)

    if library.songs.filter(pk=song.pk).exists():
        return JsonResponse(
            {"error": f"'{song.title}' is already in this library."},
            status=400,
        )

    library.songs.add(song)
    return JsonResponse(_serialize_library(library), status=200)


@csrf_exempt
@require_http_methods(["DELETE"])
def library_remove_song(request, user_id, song_id):
    user    = get_object_or_404(User, pk=user_id)
    library = get_object_or_404(Library, user=user)
    song    = get_object_or_404(Song, pk=song_id)

    if not library.songs.filter(pk=song.pk).exists():
        return JsonResponse(
            {"error": f"'{song.title}' is not in this library."},
            status=404,
        )

    library.songs.remove(song)
    return JsonResponse(
        {"message": f"'{song.title}' removed from {user.name}'s library."},
        status=200,
    )


@csrf_exempt
@require_http_methods(["DELETE"])
def library_clear(request, user_id):
    user    = get_object_or_404(User, pk=user_id)
    library = get_object_or_404(Library, user=user)

    library.songs.clear()
    return JsonResponse(
        {"message": f"{user.name}'s library has been cleared."},
        status=200,
    )


@csrf_exempt
@require_http_methods(["DELETE"])
def library_delete(request, user_id):
    user    = get_object_or_404(User, pk=user_id)
    library = get_object_or_404(Library, user=user)

    library.delete()
    return JsonResponse(
        {"message": f"{user.name}'s library has been deleted."},
        status=200,
    )
