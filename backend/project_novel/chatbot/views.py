# ★chatbot/views.py
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
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import BasePermission
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


class ChatbotView(APIView):
    """
    사용자와 대화하는 챗봇 뷰입니다.
    
    사용자의 메시지를 받아 OpenAI GPT로부터 응답을 생성하고 반환합니다.
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
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
        prompt = raw_body.strip()

        if not prompt:
            return Response({'error': 'Empty message received'}, status=400)

        # Existing logic to get a response from OpenAI
        session_conversations = request.session.get('conversations', [])
        previous_conversations = "\n".join([f"User: {c['prompt']}\nAI: {c['response']}" for c in session_conversations])
        prompt_with_previous = f"{previous_conversations}\nUser: {prompt}\nAI:"

        # model_engine = "text-davinci-003"
        # completions = openai.Completion.create(
        #     engine=model_engine,
        #     prompt=prompt_with_previous,
        #     max_tokens=1024,
        #     n=5,
        #     stop=None,
        #     temperature=0.5,
        # )
        # response = completions.choices[0].text.strip()
        
        # Response 처리 부분
        try:
            response = process_openai_request.delay(prompt_with_previous).get(timeout=30)
        except Exception as e:
            # Log the error and return a 500 response
            logger.error(f"Error processing OpenAI request: {e}")
            return Response({'error': 'Error processing request'}, status=500)

        # Saving the conversation to the database
        # 추후, user 와 admin 모두가 DB 내 대화 데이터를 관리할 수 있도록.
        conversation = Conversation(prompt=prompt, response=response)
        conversation.save()

        # Updating the session with the new conversation
        session_conversations.append({'prompt': prompt, 'response': response})
        request.session['conversations'] = session_conversations
        request.session.modified = True

        print({'prompt': prompt, 'response': response})
        return JsonResponse({'prompt': prompt, 'response': response})


    def get(self, request, *args, **kwargs):
        """
        사용자의 대화 이력을 반환합니다.
        """
        conversations = request.session.get('conversations', [])
        return JsonResponse({'conversations': conversations})
# DB 내 대화 데이터와 interacting 하도록 (하는 API). 즉, admin, user 모두 DB에 저장된 chat history 관리가능케 하는 API.
# 각 endpoint 에 대한 CRUD 작업을 수행하는 API. (기존 viewsets.ModelViewSet 을 View 로 통일화 및 대체)


class ConversationView(View):
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
