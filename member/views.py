from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from django.db import IntegrityError
from django.urls import reverse
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.views import View
from django.utils.decorators import method_decorator

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import viewsets

from .forms import NewProfileChangeForm
from allauth.socialaccount.helpers import render_authentication_error

from elasticsearch import Elasticsearch
from elastic_app_search import Client
from sentence_transformers import SentenceTransformer, util
import re
import json
import datetime

from social_django.views import complete
from .models import LegalQAFinal
from .serializers import LegalQAFinalSerializer
from datetime import datetime, timedelta 

admin.site.register(Token)

# Elasticsearch 클라이언트 설정
es_cloud_id = "lowlaw:YXAtbm9ydGhlYXN0LTIuYXdzLmVsYXN0aWMtY2xvdWQuY29tOjQ0MyQ2YzNmMjA4MmNiMzk0M2YxYTBiZWI0ZDY2M2JmM2VlZCRjZTA2NGZhNjFiMmI0N2Y0ODgzMjY0Y2FlMzVlZDgxZQ=="
es_username = "elastic"
es_pw = "LWkW2eILoZYZylsDDThLaCKY"
es = Elasticsearch(cloud_id=es_cloud_id, basic_auth=(es_username, es_pw))

# Appsearch 클라이언트 설정
client = Client(
    base_endpoint="lowlaw.ent.ap-northeast-2.aws.elastic-cloud.com/api/as/v1",
    api_key="private-egnzqo7tt7fd6fngz13mmox9",
    use_https=True
)

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
        except IntegrityError as e:
            messages.error(request, '이미 등록된 이메일입니다.')
            return redirect('register')
        else:
            messages.success(request, '회원가입이 완료되었습니다. 로그인해주세요.')
            return redirect('login')
    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            token_key = token.key
            expires_at = token.created + timedelta(days=1)
            response_data = {
                'access_token': token_key,
                'access_token_expires': expires_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': '이메일과 비밀번호가 일치하지 않습니다.'}, status=400)
    elif request.method == 'GET':
        return render(request, 'login.html')
    return JsonResponse({'error': 'POST 요청이 필요합니다.'}, status=400)

class CustomAuthToken(ObtainAuthToken):
    def custom_auth_token(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key})

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def user_admin(request):
    if not request.user.is_superuser:
        return redirect('home')
    users = User.objects.all()
    return render(request, 'user_admin.html', {'users': users})

@login_required
def mypage(request):
    user = request.user

    if request.method == 'POST':
        profile_form = NewProfileChangeForm(request.POST, instance=user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, '사용자 정보가 수정되었습니다.')
    else:
        profile_form = NewProfileChangeForm(instance=user)
    
    return render(request, 'mypage.html', {'user': user, 'profile_form': profile_form})

@login_required
def user_delete(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, '회원 탈퇴가 완료되었습니다.')
        return render(request, 'user_delete.html', {'is_deleted': True})
    
    return render(request, 'user_delete.html', {'is_deleted': False})