# from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User

class UserViewSetTest(APITestCase):
    # 사용자 생성에 대한 테스트 케이스
    def test_create_user(self):
        # 사용자 생성을 위한 URL 엔드포인트
        url = reverse('users-list')
        
        # 테스트 요청에 사용될 데이터 (username과 password만 필요)
        data = {'username': 'testuser', 'password': 'testpassword'}
        
        # POST 요청을 사용하여 사용자 생성
        response = self.client.post(url, data, format='json')
        
        # 응답 상태 코드가 201 Created인지 확인 (성공적인 생성을 나타냄)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 데이터베이스에 정확히 하나의 사용자 객체가 생성되었는지 확인
        self.assertEqual(User.objects.count(), 1)

    # 사용자 목록 조회에 대한 테스트 케이스
    def test_list_users(self):
        # 사용자 목록 조회를 위한 URL 엔드포인트
        url = reverse('users-list')
        
        # GET 요청을 사용하여 사용자 목록 조회
        response = self.client.get(url)
        
        # 응답 상태 코드가 200 OK인지 확인 (성공적인 조회를 나타냄)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # 추가적으로 특정 사용자 조회, 사용자 정보 수정, 사용자 삭제에 대한 테스트 케이스를 작성할 수 있음
