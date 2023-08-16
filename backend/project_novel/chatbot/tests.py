from django.test import TestCase

# tests.py -> urls.py -> call views.py (how test works)

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class ChatbotViewTest(APITestCase):
    # ChatbotView에 대한 테스트 케이스
    def test_chat_response(self):
        user = User.objects.create_user(username='dolos', password='test')
        self.client = APIClient()

        # Token을 생성하고 요청 헤더에 추가
        tokens = get_tokens_for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + tokens['access'])

        
        url = reverse('chatbot')

        # 테스트에 사용할 요청 데이터를 정의.
        data = {'message': '이 메세지를 받았다면 "chatbot app, 테스트 케이스 통과입니다." 이라고 답변해보세요.'}


        # 지정된 URL에 POST 요청을 보냅니다.
        # views.py 파일의 ChatbotView 클래스의 post 메서드가 호출됩니다.
        response = self.client.post(url, data, format='json')

        # 응답 내용 출력 (디버깅용)
        print(response.content.decode())

        # 응답 상태 코드가 200 OK인지 확인.
        # HTTP 상태 코드 200은 요청이 성공적으로 처리되었음을 나타냅니다.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 필요한 경우, 추가적인 응답 내용 검증을 수행할 수 있습니다.
        # 예를 들어, 응답 데이터의 구조나 값 등을 검증할 수 있습니다.


