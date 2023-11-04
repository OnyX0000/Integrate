from django.http import JsonResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from social_django.views import complete
from allauth.socialaccount.helpers import render_authentication_error

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError

import json
from datetime import datetime, timedelta

# 회원가입 API
@api_view(['POST'])
@permission_classes([AllowAny])
def api_register(request):
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body)
            username = request_data.get('username')
            email = request_data.get('email')
            password = request_data.get('password')
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data in the request'}, status=400)
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
        except IntegrityError as e:
            return JsonResponse({'error': 'Already Registered Email'}, status=400)
        return JsonResponse({'message': 'Register Success'})
    return JsonResponse({'error': 'Invalid Request'}, status=400)

# 로그인 API
@api_view(['POST'])
def api_login(request):
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body)
            email = request_data.get('email')
            password = request_data.get('password')
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data in the request'}, status=400)
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            token_key = token.key
            expires_at = token.created + timedelta(days=1)
            response_data = {
                'access_token': token_key,
                'access_token_expires': (token.created + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': 'Email and Password NOT MATCH'}, status=400)
    else:
        return JsonResponse({'error': 'POST request is required.'}, status=400)

# 로그아웃 API
@api_view(['POST'])
def api_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({'message': '로그아웃 성공'})
    else:
        return JsonResponse({'error': '로그인되어 있지 않습니다.'}, status=400)

# 관리자 모드 API
@api_view(['GET'])
def api_admin(request):
    if not request.user.is_superuser:
        return JsonResponse({'error': '관리자 권한이 필요합니다.'}, status=403)
    
    users = User.objects.all()
    # 사용자 정보를 JSON 형식으로 반환
    user_data = [{'username': user.username, 'email': user.email} for user in users]
    return JsonResponse({'users': user_data})

# 회원 탈퇴 API
@api_view(['POST'])
def api_user_delete(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            request.user.delete()
            return JsonResponse({'message': '회원 탈퇴가 완료되었습니다.'})
        else:
            return JsonResponse({'error': '로그인되어 있지 않습니다.'}, status=400)

# 마이페이지 API
@api_view(['GET', 'POST'])
def api_mypage(request):
    if request.method == 'GET':
        user = request.user
        if user.is_authenticated:
            # 사용자 정보를 JSON 형식으로 반환
            user_data = {'username': user.username, 'email': user.email}
            return JsonResponse(user_data)
        else:
            return JsonResponse({'error': '로그인되어 있지 않습니다.'}, status=400)
    elif request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            profile_form = NewProfileChangeForm(request.data, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                return JsonResponse({'message': '사용자 정보가 수정되었습니다.'})
            else:
                return JsonResponse({'error': '잘못된 데이터가 포함되어 있습니다.'}, status=400)
        else:
            return JsonResponse({'error': '로그인되어 있지 않습니다.'}, status=400)