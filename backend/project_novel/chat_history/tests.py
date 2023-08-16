from django.test import TestCase
from chat_history.models import ChatHistory
from rest_framework.test import APITestCase
from users.models import User

class ChatHistoryTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        self.prompt = 'Hello, how are you?'
        self.response = 'I am fine, thank you!'
        self.chat_history = ChatHistory.objects.create(user=self.user, prompt=self.prompt, response=self.response)

        # 테스트 유저 생성
        user = User.objects.create_user(username='dolos', password='test')

        # 테스트 채팅 내역 생성
        self.prompt = "Hello, how are you?"
        self.response = "I'm good, thank you!"
        self.chat_history = ChatHistory.objects.create(user=self.user, prompt=self.prompt, response=self.response)

    def test_chat_history_creation(self):
        # ChatHistory 모델에서 데이터를 조회
        retrieved_chat = ChatHistory.objects.filter(user=self.user).first()
        self.assertEqual(retrieved_chat.prompt, self.prompt)
        self.assertEqual(retrieved_chat.response, self.response)

    def test_chat_history_retrieval(self):
        # ChatHistory 모델에서 데이터를 조회
        retrieved_chat = ChatHistory.objects.filter(user=self.user).first()
        self.assertEqual(retrieved_chat.prompt, self.prompt)
        self.assertEqual(retrieved_chat.response, self.response)
