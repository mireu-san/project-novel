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

    def test_chat_history_creation(self):
        # ChatHistory 객체를 조회
        retrieved_chat = ChatHistory.objects.get(user=self.user)
        self.assertEqual(retrieved_chat.prompt, self.prompt)
        self.assertEqual(retrieved_chat.response, self.response)

    def test_chat_history_retrieval(self):
        # ChatHistory 객체를 조회
        retrieved_chat = ChatHistory.objects.get(user=self.user)
        self.assertEqual(retrieved_chat.prompt, self.prompt)
        self.assertEqual(retrieved_chat.response, self.response)
