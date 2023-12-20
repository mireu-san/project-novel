from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.serializers import AuthTokenSerializer
import requests
from django.conf import settings


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
    def get(self, request):
        code = request.GET.get("code")
        try:
            token_response = requests.post(
                "https://kauth.kakao.com/oauth/token",
                data={
                    "grant_type": "authorization_code",
                    "client_id": settings.KAKAO_REST_API_KEY,
                    "redirect_uri": "http://localhost:5173/auth/kakao/callback",
                    "code": code,
                },
            )
            token_response_data = token_response.json()
            access_token = token_response_data["access_token"]

            user_info_response = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            user_info_data = user_info_response.json()

            email = user_info_data.get("kakao_account", {}).get("email", "")
            if not email:
                return Response(
                    {"error": "Email not provided"}, status=status.HTTP_400_BAD_REQUEST
                )

            user_model = get_user_model()
            user, created = user_model.objects.get_or_create(email=email)
            if created:
                user.set_password(user_model.objects.make_random_password())
                user.save()

            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            )
        except KeyError:
            return Response(
                {"error": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
