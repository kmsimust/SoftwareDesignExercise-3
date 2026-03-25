from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Song


@require_http_methods(["GET"])
def song_list(request):
    songs = Song.objects.all()

    # Optional filtering
    occasion   = request.GET.get("occasion")
    mood_tone  = request.GET.get("mood_tone")
    genre      = request.GET.get("genre")

    if occasion:
        songs = songs.filter(occasion__icontains=occasion)
    if mood_tone:
        songs = songs.filter(mood_tone__icontains=mood_tone)
    if genre:
        songs = songs.filter(genre__icontains=genre)

    data = [_serialize(song) for song in songs]
    return JsonResponse(data, safe=False, status=200)


@require_http_methods(["GET"])
def song_detail(request, pk):
    song = get_object_or_404(Song, pk=pk)
    return JsonResponse(_serialize(song), status=200)


@csrf_exempt
@require_http_methods(["POST"])
def song_create(request):
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body."}, status=400)

    required_fields = [
        "title", "occasion", "mood_tone", "genre",
        "singer_voice", "meaning", "song_durations",
    ]
    missing = [f for f in required_fields if f not in body]
    if missing:
        return JsonResponse(
            {"error": f"Missing required fields: {', '.join(missing)}"},
            status=400,
        )

    try:
        song = Song.objects.create(
            title          = body["title"],
            occasion       = body["occasion"],
            mood_tone      = body["mood_tone"],
            genre          = body["genre"],
            singer_voice   = body["singer_voice"],
            meaning        = body["meaning"],
            song_durations = body["song_durations"],  # "HH:MM:SS"
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse(_serialize(song), status=201)


@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def song_update(request, pk):
    song = get_object_or_404(Song, pk=pk)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body."}, status=400)

    updatable_fields = [
        "title", "occasion", "mood_tone", "genre",
        "singer_voice", "meaning", "song_durations",
    ]

    if request.method == "PUT":
        # Full update — all fields must be present
        missing = [f for f in updatable_fields if f not in body]
        if missing:
            return JsonResponse(
                {"error": f"Missing required fields for full update: {', '.join(missing)}"},
                status=400,
            )

    # Apply whichever fields are present
    for field in updatable_fields:
        if field in body:
            setattr(song, field, body[field])

    try:
        song.save()
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse(_serialize(song), status=200)


@csrf_exempt
@require_http_methods(["DELETE"])
def song_delete(request, pk):
    song = get_object_or_404(Song, pk=pk)
    song.delete()
    return JsonResponse({"message": f"Song '{song.title}' deleted successfully."}, status=200)


def _serialize(song: Song) -> dict:
    return {
        "id":             song.pk,
        "title":          song.title,
        "occasion":       song.occasion,
        "mood_tone":      song.mood_tone,
        "genre":          song.genre,
        "singer_voice":   song.singer_voice,
        "meaning":        song.meaning,
        "song_durations": str(song.song_durations),  # TimeField → "HH:MM:SS"
    }