from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

# DefaultRouter를 사용하여 뷰셋과 연결된 URL 패턴을 자동으로 생성
router = DefaultRouter()
router.register(r'', UserViewSet, basename='users')

urlpatterns = [
    # 라우터에서 생성된 URL 패턴을 포함
    # 이것은 UserViewSet에 대한 CRUD 엔드포인트를 자동으로 설정합니다.
    path('', include(router.urls)),
]
