# You are viewing a ☆root folder's urls.py

from django.contrib import admin
# re_path - regular expression path
from django.urls import path, re_path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg       import openapi

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Light Novel GPT",
        default_version='v1.0',
        description="라이트 노벨 추천하는 GPT 기반의 챗봇 API 서버.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="starmireu@gmail.com"),
        license=openapi.License(name="mit"),
    ),
    public=True,
    # ★May check back later - this may better to be admin users only
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path('^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-root'),
    re_path(r'redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
    
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
