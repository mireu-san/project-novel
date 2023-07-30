# users/views.py


from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # 비밀번호 암호화 저장
        user.set_password(request.data['password'])
        user.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User created successfully",
        }, status=status.HTTP_201_CREATED)
