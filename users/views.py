from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import (
    RefreshToken,
    OutstandingToken,
    BlacklistedToken,
)
from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.serializers import AuthTokenSerializer
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


# 사용자가 자신의 프로필 또는 관리자가 모든 프로필을 확인, 수정, 삭제할 수 있는 권한 클래스를 정의합니다.
class IsSelfOrAdmin(BasePermission):
    """사용자는 자신의 프로필만 확인, 수정, 삭제할 수 있습니다. 관리자는 모든 프로필을 확인, 수정, 삭제할 수 있습니다."""

    def has_object_permission(self, request, view, obj):
        if request.user == obj or request.user.is_staff:
            return True
        return False


# 사용자 정보를 CRUD(생성, 읽기, 업데이트, 삭제)하는 API 엔드포인트를 정의하는 뷰셋 클래스입니다.
class UserViewSet(viewsets.ModelViewSet):
    """사용자 정보를 CRUD하는 API 엔드포인트"""

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """해당 액션에 대한 권한 클래스를 반환합니다."""
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


# 새로운 사용자를 등록하는 API 엔드포인트를 정의하는 뷰 클래스입니다.
class SignupView(CreateAPIView):
    """새로운 사용자를 등록하는 API 엔드포인트"""

    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data["password"])
        user.save()


# 사용자가 로그인하고 토큰을 받는 API 엔드포인트를 정의하는 뷰 클래스입니다.
class LoginView(APIView):
    """로그인하고 토큰을 받는 API 엔드포인트"""

    serializer_class = AuthTokenSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=AuthTokenSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user_id": user.pk,
                "username": user.username,
            }
        )


# 사용자가 로그아웃하고 토큰을 삭제하는 API 엔드포인트를 정의하는 뷰 클래스입니다.
class LogoutView(APIView):
    """로그아웃하고 토큰을 삭제하는 API 엔드포인트"""

    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
        except Token.DoesNotExist:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class VerifyAuthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        is_authenticated = request.user.is_authenticated
        return Response({"isAuthenticated": is_authenticated})


# 카카오 로그인 뷰
class KakaoLoginView(APIView):
    def post(self, request):
        # Extract the authorization code from the request data
        code = request.data.get("code")

        if not code:
            return Response(
                {"error": "No authorization code provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Request to exchange the authorization code for an access token
            token_response = requests.post(
                "https://kauth.kakao.com/oauth/token",
                data={
                    "grant_type": "authorization_code",
                    "client_id": settings.KAKAO_REST_API_KEY,
                    "client_secret": settings.KAKAO_CLIENT_SECRET,  # Include client secret
                    "redirect_uri": settings.KAKAO_REDIRECT_URI,
                    "code": code,
                },
            )
            token_response_data = token_response.json()

            # Check for error in token response
            if "error" in token_response_data:
                return Response(token_response_data, status=status.HTTP_400_BAD_REQUEST)

            access_token = token_response_data.get("access_token")

            # Use access token to request user information from Kakao
            user_info_response = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            user_info_data = user_info_response.json()

            # Extract email from user information
            email = user_info_data.get("kakao_account", {}).get("email")
            if not email:
                return Response(
                    {"error": "Kakao account does not provide an email"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Get or create a user based on the email
            User = get_user_model()
            user, created = User.objects.get_or_create(email=email)

            # If the user is created, set an unusable password
            if created:
                user.set_unusable_password()
                user.save()

            # Create JWT tokens for the user
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            )

        except Exception as e:
            # Return a response in case of any exception
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class KakaoLogoutView(APIView):
    """
    카카오 로그아웃을 처리하는 API 엔드포인트
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 로컬 JWT 토큰 무효화
        try:
            tokens = OutstandingToken.objects.filter(user=request.user)
            for token in tokens:
                BlacklistedToken.objects.get_or_create(token=token)

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
