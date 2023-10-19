# users/views.py 파일

# 필요한 모듈과 클래스를 불러옵니다.
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
# from rest_framework.authtoken.views import APIView
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.serializers import AuthTokenSerializer

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
    queryset = get_user_model().objects.all()  # 모든 사용자 객체를 쿼리셋으로 가져옵니다.
    serializer_class = UserSerializer  # 사용자 데이터를 직렬화/역직렬화하기 위한 시리얼라이저 클래스를 지정합니다.

    def get_permissions(self):
        """해당 액션에 대한 권한 클래스를 반환합니다."""
        permission_classes = [AllowAny]  # 모든 사용자에게 권한을 부여합니다.
        return [permission() for permission in permission_classes]

# 새로운 사용자를 등록하는 API 엔드포인트를 정의하는 뷰 클래스입니다.
class SignupView(CreateAPIView):
    """새로운 사용자를 등록하는 API 엔드포인트"""
    serializer_class = UserSerializer  # 사용자 데이터를 직렬화/역직렬화하기 위한 시리얼라이저 클래스를 지정합니다.
    permission_classes = (AllowAny,)  # 모든 사용자에게 권한을 부여합니다.

    # POST 요청을 처리하는 메소드입니다.
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  # 요청 데이터를 시리얼라이저에 전달합니다.
        serializer.is_valid(raise_exception=True)  # 데이터 유효성을 검사하고, 유효하지 않으면 예외를 발생시킵니다.
        self.perform_create(serializer)  # 유효한 데이터로 사용자 객체를 생성합니다.
        headers = self.get_success_headers(serializer.data)  # 성공 응답의 헤더를 가져옵니다.
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)  # 생성된 사용자 데이터와 201 Created 상태 코드를 반환합니다.

    # 사용자 객체를 생성하는 메소드입니다.
    def perform_create(self, serializer):
        user = serializer.save()  # 시리얼라이저를 사용하여 사용자 객체를 생성하고 저장합니다.
        user.set_password(serializer.validated_data['password'])  # 비밀번호를 해시화하여 저장합니다.
        user.save()  # 변경된 내용을 데이터베이스에 저장합니다.

# 사용자가 로그인하고 토큰을 받는 API 엔드포인트를 정의하는 뷰 클래스입니다.
class LoginView(APIView):
    """로그인하고 토큰을 받는 API 엔드포인트"""
    serializer_class = AuthTokenSerializer  # 클래스 레벨 변수로 serializer_class를 설정
    permission_classes = (AllowAny,)
    
    @swagger_auto_schema(request_body=AuthTokenSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})  # 요청 데이터를 시리얼라이저에 전달합니다.
        serializer.is_valid(raise_exception=True)  # 데이터 유효성을 검사하고, 유효하지 않으면 예외를 발생시킵니다.
        user = serializer.validated_data['user']  # 유효한 데이터에서 사용자 객체를 가져옵니다.
        refresh = RefreshToken.for_user(user)  # 사용자를 위한 새로운 토큰 쌍을 생성합니다.
        return Response({
            'access': str(refresh.access_token),  # 접근 토큰을 반환합니다.
            'refresh': str(refresh),  # 새로고침 토큰을 반환합니다.
            'user_id': user.pk,  # 사용자의 ID를 반환합니다.
            'username': user.username,  # 사용자의 이름을 반환합니다.
        })

# 사용자가 로그아웃하고 토큰을 삭제하는 API 엔드포인트를 정의하는 뷰 클래스입니다.
class LogoutView(APIView):
    """로그아웃하고 토큰을 삭제하는 API 엔드포인트"""
    # permission_classes = (IsAuthenticated,)  # 인증된 사용자에게만 권한을 부여합니다.
    permission_classes = (AllowAny,)

    # POST 요청을 처리하는 메소드입니다.
    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)  # 현재 사용자의 토큰을 가져옵니다.
            token.delete()  # 토큰을 삭제합니다.
        except Token.DoesNotExist:
            pass  # 토큰이 없는 경우에는 처리를 하지 않습니다.

        return Response(status=status.HTTP_204_NO_CONTENT)  # 204 No Content 상태 코드를 반환합니다.
