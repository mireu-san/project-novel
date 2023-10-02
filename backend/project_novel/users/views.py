# users/views.py

from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token


# 메모: view 로 할까 싶었지만, 특별히 커스텀화가 요구되는게 아닌 이상 viewsets 으로 설정.
class IsSelfOrAdmin(BasePermission):
    """사용자는 자신의 프로필만 확인, 수정, 삭제할 수 있습니다. 관리자는 모든 프로필을 확인, 수정, 삭제할 수 있습니다."""
    def has_object_permission(self, request, view, obj):
        # Allow user to view/update/delete their own profile
        if request.user == obj:
            return True
        # Allow admins to view/update/delete any profile
        if request.user.is_staff:
            return True
        return False

class UserViewSet(viewsets.ModelViewSet):
    """사용자 정보를 CRUD하는 API 엔드포인트"""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """해당 액션에 대한 권한 클래스를 반환합니다."""
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsSelfOrAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class SignupView(CreateAPIView):
    """새로운 사용자를 등록하는 API 엔드포인트"""
    serializer_class = UserSerializer


class LoginView(ObtainAuthToken):
    """로그인하고 토큰을 받는 API 엔드포인트"""
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
        })
    

class LogoutView(APIView):
    """로그아웃하고 토큰을 삭제하는 API 엔드포인트"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        # CAUTION: probably the user is not logged out here, only the token is deleted?
        return Response(status=status.HTTP_204_NO_CONTENT)