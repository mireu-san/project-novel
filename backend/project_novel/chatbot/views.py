# ★chatbot/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import openai
import os
import json
from .models import Conversation
from rest_framework import viewsets
from .serializers import ConversationSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import logging
from celeryapp.tasks import process_openai_request

logger = logging.getLogger('django')

load_dotenv()

# API KEY 를 환경변수로부터 불러옵니다.
openai.api_key = os.getenv('OPENAI_API_KEY')

# 최종 단계에서 활성화 및 구성 예정
# https://platform.openai.com/docs/libraries/python-library
# chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world"}])

@method_decorator(csrf_exempt, name='dispatch')
# 유저가 장고 서버를 통해 interatcion 하도록.


class ChatbotView(LoginRequiredMixin, APIView):
    """
    사용자와 대화하는 챗봇 뷰입니다.
    
    사용자의 메시지를 받아 OpenAI GPT로부터 응답을 생성하고 반환합니다.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': '로그인을 먼저 하세요!'}, status=401)
        """
        사용자와 대화하는 챗봇 뷰입니다.
        
        사용자의 메시지를 받아 OpenAI GPT로부터 응답을 생성하고 반환합니다.
        """
        
        logger.info('Post method entered')

        # Logging the raw request body

        # Prompt 처리 부분
        raw_body = request.body.decode('utf-8')
        print("Received request body:", raw_body)

        # Assuming the raw_body is a plain string message from the user
        user_message = raw_body.strip()

        if not user_message:
            return Response({'error': 'Empty message received'}, status=400)

        # Predefined prompt
        predefined_prompt = {
            "role": "system",
            "content": "You are an anime expert. Your role is to listen to a user input and based on his/her expression, suggest any anime, light novel, visual novel or manga for this user."
        }

        # User message
        user_input = {
            "role": "user",
            "content": user_message
        }

        # Preparing the messages parameter
        messages = [predefined_prompt, user_input]

        # Response 처리 부분
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            response_text = response['choices'][0]['message']['content']
        except Exception as e:
            # Log the error and return a 500 response
            logger.error(f"Error processing OpenAI request: {e}")
            return Response({'error': 'Error processing request'}, status=500)

        # Saving the conversation to the database
        # 추후, user 와 admin 모두가 DB 내 대화 데이터를 관리할 수 있도록.
        conversation = Conversation(prompt=user_message, response=response_text)
        conversation.save()

        # Updating the session with the new conversation
        session_conversations = request.session.get('conversations', [])
        session_conversations.append({'prompt': user_message, 'response': response_text})
        request.session['conversations'] = session_conversations
        request.session.modified = True

        print({'prompt': user_message, 'response': response_text})
        return JsonResponse({'prompt': user_message, 'response': response_text})

    def get(self, request, *args, **kwargs):
        """
        사용자의 대화 이력을 반환합니다.
        """
        conversations = request.session.get('conversations', [])
        return JsonResponse({'conversations': conversations})


class ConversationView(LoginRequiredMixin, View):
    """
    대화 내역을 데이터베이스에서 조회, 추가, 삭제하는 API 뷰입니다.
    
    관리자 및 사용자는 이 API를 통해 저장된 대화 내역을 관리할 수 있습니다.
    """
    def get(self, request, pk=None, *args, **kwargs):
        """
        특정 대화 또는 모든 대화의 내역을 조회합니다.
        """
        # 특정 대화(pk)를 조회하거나 전체 대화 목록을 반환합니다.
        if pk:
            conversation = Conversation.objects.get(pk=pk) # 특정 대화 조회
            serializer = ConversationSerializer(conversation)
            return JsonResponse(serializer.data)
        else:
            conversations = Conversation.objects.all() # 전체 대화 목록 조회
            serializer = ConversationSerializer(conversations, many=True)
            return JsonResponse(serializer.data, safe=False)

    def post(self, request, *args, **kwargs):
        """
        새로운 대화 내역을 데이터베이스에 저장합니다.
        """
        # 새로운 대화를 생성합니다.
        data = json.loads(request.body)
        serializer = ConversationSerializer(data=data)
        if serializer.is_valid():
            serializer.save() # 데이터가 유효하면 저장
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400) # 유효하지 않으면 오류 반환

    def delete(self, request, pk, *args, **kwargs):
        """
        특정 대화 내역을 데이터베이스에서 삭제합니다.
        """
        # 특정 대화(pk)를 삭제합니다.
        conversation = Conversation.objects.get(pk=pk)
        conversation.delete() # 대화 삭제
        return JsonResponse({'message': 'Deleted successfully'}, status=204) # 성공 메시지 반환
