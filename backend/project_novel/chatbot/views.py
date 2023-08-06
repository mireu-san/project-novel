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

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


@method_decorator(csrf_exempt, name='dispatch')
# 유저가 장고 서버를 통해 interatcion 하도록.
class ChatbotView(View):
    def post(self, request, *args, **kwargs):
        # 요청 본문 로깅
        print("Received request body:", request.body.decode('utf-8'))

        body = json.loads(request.body.decode('utf-8'))
        # 'messages' key 가 있는지 없는지 확인.
        # messages = body['messages']
        messages = body.get('messages', [])
        if not messages:
            return JsonResponse({'error': '에러 코드 400, client side 에서 어떠한 메세지를 받지 못함.'}, status=400)

        # 들어오는 value가 없을 시, 예외 처리
        prompt = None
        response = None

        for message in messages:
            if message['role'] == 'user':
                prompt = message['content']

        if prompt:
            # 이전 대화 기록 가져오기
            session_conversations = request.session.get('conversations', [])
            previous_conversations = "\n".join([f"User: {c['prompt']}\nAI: {c['response']}" for c in session_conversations])
            prompt_with_previous = f"{previous_conversations}\nUser: {prompt}\nAI:"

            model_engine = "text-davinci-003"
            completions = openai.Completion.create(
                engine=model_engine,
                prompt=prompt_with_previous,
                max_tokens=1024,
                n=5,
                stop=None,
                temperature=0.5,
            )
            response = completions.choices[0].text.strip()

            conversation = Conversation(prompt=prompt, response=response)
            conversation.save()

            # 대화 기록에 새로운 응답 추가
            session_conversations.append({'prompt': prompt, 'response': response})
            request.session['conversations'] = session_conversations
            # 세변 내용 변경 시, 내용을 추가로 SQLite 에 저장
            request.session.modified = True

        print({'prompt': prompt, 'response': response})
        return JsonResponse({'prompt': prompt, 'response': response})

    def get(self, request, *args, **kwargs):
        conversations = request.session.get('conversations', [])
        return JsonResponse({'conversations': conversations})
# DB 내 대화 데이터와 interacting 하도록 (하는 API). 즉, admin, user 모두 DB에 저장된 chat history 관리가능케 하는 API.
# 각 endpoint 에 대한 CRUD 작업을 수행하는 API. (기존 viewsets.ModelViewSet 을 View 로 통일화 및 대체)
class ConversationView(View):
    def get(self, request, pk=None, *args, **kwargs):
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
        # 새로운 대화를 생성합니다.
        data = json.loads(request.body)
        serializer = ConversationSerializer(data=data)
        if serializer.is_valid():
            serializer.save() # 데이터가 유효하면 저장
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400) # 유효하지 않으면 오류 반환

    def put(self, request, pk, *args, **kwargs):
        # 특정 대화(pk)를 수정합니다.
        conversation = Conversation.objects.get(pk=pk)
        data = json.loads(request.body)
        serializer = ConversationSerializer(conversation, data=data)
        if serializer.is_valid():
            serializer.save() # 데이터가 유효하면 저장
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400) # 유효하지 않으면 오류 반환

    def delete(self, request, pk, *args, **kwargs):
        # 특정 대화(pk)를 삭제합니다.
        conversation = Conversation.objects.get(pk=pk)
        conversation.delete() # 대화 삭제
        return JsonResponse({'message': 'Deleted successfully'}, status=204) # 성공 메시지 반환
