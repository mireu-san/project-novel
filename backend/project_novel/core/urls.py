# You are viewing a ☆root folder's urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # 관리자 사이트에 대한 URL 설정
    path('admin/', admin.site.urls),

    # chatbot 앱의 URL 설정 포함
    # chatbot.urls 파일에 정의된 URL 패턴을 해당 경로 아래로 포함시킴
    path('chatbot/', include('chatbot.urls')),

    # users 앱의 URL 설정 포함
    # users.urls 파일에 정의된 URL 패턴을 해당 경로 아래로 포함시킴
    path('users/', include('users.urls')),

    # JWT 인증 토큰을 받기 위한 엔드포인트
    # 사용자가 로그인 정보를 제공하면, 해당 사용자에 대한 인증 토큰을 반환함
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # 기존 JWT 인증 토큰을 새로 고침하기 위한 엔드포인트
    # 토큰의 유효 기간이 만료되기 전에 새로운 토큰을 요청할 수 있게 해줌
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
