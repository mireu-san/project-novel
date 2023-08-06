from django.test import TestCase

# tests.py -> urls.py -> call views.py (how test works)

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class ChatbotViewTest(APITestCase):
    # ChatbotView에 대한 테스트 케이스
    def test_chat_response(self):
        # 'chatbot' 이름의 URL 패턴을 찾아서 실제 URL을 얻습니다.
        # urls.py 파일에서 'chatbot' 이름으로 정의된 URL 패턴과 연결됩니다.
        url = reverse('chatbot')

        # 테스트에 사용할 요청 데이터를 정의.
        data = {'messages': [{'role': 'user', 'content': 'Hello, AI!'}]}

        # 지정된 URL에 POST 요청을 보냅니다.
        # views.py 파일의 ChatbotView 클래스의 post 메서드가 호출됩니다.
        response = self.client.post(url, data, format='json')

        # 응답 상태 코드가 200 OK인지 확인.
        # HTTP 상태 코드 200은 요청이 성공적으로 처리되었음을 나타냅니다.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 필요한 경우, 추가적인 응답 내용 검증을 수행할 수 있습니다.
        # 예를 들어, 응답 데이터의 구조나 값 등을 검증할 수 있습니다.
