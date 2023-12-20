from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    LoginView,
    LogoutView,
    SignupView,
    VerifyAuthView,
    KakaoLoginView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# DefaultRouter를 사용하여 뷰셋과 연결된 URL 패턴을 자동으로 생성
router = DefaultRouter()
router.register(r"", UserViewSet, basename="users")

urlpatterns = [
    # 라우터에서 생성된 URL 패턴을 포함
    # 이것은 UserViewSet에 대한 CRUD 엔드포인트를 자동으로 설정합니다.
    path("", include(router.urls)),
    path("users/login/", LoginView.as_view(), name="login"),
    path("users/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("users/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/logout/", LogoutView.as_view(), name="logout"),
    path("users/signup/", SignupView.as_view(), name="signup"),
    path("users/verify_auth/", VerifyAuthView.as_view(), name="verify_auth"),
    # social login
    path("auth/kakao/", KakaoLoginView.as_view(), name="kakao_login"),
]
