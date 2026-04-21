from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import jwt
from datetime import datetime, timedelta

from .models import User
from library.models import Library

SECRET_KEY = "your-secret-key-change-this"  # Use Django settings.SECRET_KEY in production


def _serialize(user):
    return {
        "id":    user.pk,
        "name":  user.name,
        "email": user.email,
    }


def _generate_token(user):
    """Generate JWT token for user"""
    payload = {
        'user_id': user.pk,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(days=7),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


@csrf_exempt
@require_http_methods(["POST"])
def user_login(request):
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body."}, status=400)

    email = body.get("email")

    if not email:
        return JsonResponse({"error": "email is required."}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    token = _generate_token(user)
    return JsonResponse({
        "message": "Login successful",
        "token": token,
        "user": _serialize(user)
    }, status=200)


@require_http_methods(["GET"])
def user_list(request):
    users = User.objects.all()

    name = request.GET.get("name")
    if name:
        users = users.filter(name__icontains=name)

    return JsonResponse([_serialize(u) for u in users], safe=False, status=200)


@require_http_methods(["GET"])
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return JsonResponse(_serialize(user), status=200)


@csrf_exempt
@require_http_methods(["POST"])
def user_create(request):
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body."}, status=400)

    name  = body.get("name")
    email = body.get("email")

    if not name or not email:
        return JsonResponse({"error": "name and email are required."}, status=400)

    if User.objects.filter(email=email).exists():
        return JsonResponse({"error": "A user with this email already exists."}, status=400)

    user = User.objects.create(name=name, email=email)
    
    # Create library for the user
    Library.objects.create(user=user)
    
    token = _generate_token(user)
    return JsonResponse({
        "message": "User created successfully",
        "token": token,
        "user": _serialize(user)
    }, status=201)


@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body."}, status=400)

    if request.method == "PUT":
        if not body.get("name") or not body.get("email"):
            return JsonResponse({"error": "name and email are required for full update."}, status=400)

    if "name" in body:
        user.name = body["name"]

    if "email" in body:
        if User.objects.filter(email=body["email"]).exclude(pk=pk).exists():
            return JsonResponse({"error": "A user with this email already exists."}, status=400)
        user.email = body["email"]

    try:
        user.save()
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse(_serialize(user), status=200)


@csrf_exempt
@require_http_methods(["DELETE"])
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    name = user.name
    user.delete()
    return JsonResponse({"message": f"User '{name}' deleted successfully."}, status=200)