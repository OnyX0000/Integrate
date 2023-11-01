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

# 토큰 발급
@api_view(['POST'])
@permission_classes([AllowAny])
def custom_auth_token(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            # data 키에 'token'을 사용하여 토큰 반환
            return JsonResponse({'access_token': token.key, 'expired_in': token.get_expires()})
        else:
            return JsonResponse({'error': '이메일과 비밀번호가 일치하지 않습니다.'}, status=400)

#토큰 유효성 검증
def validate_token(token_key):
    try:
        token = Token.objects.get(key=token_key)
        return token.user  # 토큰이 유효한 경우 해당 사용자 반환
    except Token.DoesNotExist:
        return None  # 토큰이 유효하지 않은 경우 None 반환

# 로그인 API
@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            #login(request, user)
            return JsonResponse({'message': '로그인 성공'})
        else:
            return JsonResponse({'error': '이메일과 비밀번호가 일치하지 않습니다.'}, status=400)

# 로그아웃 API
@api_view(['POST'])
def api_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({'message': '로그아웃 성공'})
    else:
        return JsonResponse({'error': '로그인되어 있지 않습니다.'}, status=400)

# 회원가입 API
@api_view(['POST'])
@permission_classes([AllowAny])
def api_register(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
        except IntegrityError as e:
            return JsonResponse({'error': '이미 등록된 이메일입니다.'}, status=400)
        else:
            return JsonResponse({'message': '회원가입이 완료되었습니다. 로그인해주세요.'})

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