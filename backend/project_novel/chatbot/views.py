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
# from django.views.generic import TemplateView

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

@method_decorator(csrf_exempt, name='dispatch')
class ChatbotView(View):
    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        # print(type(body)) # type 확인. client 측에서 오는 데이터 type 이 list 인지 dict 인지.
        # prompt = body.get('prompt')
        messages = body['messages']

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

        return JsonResponse({'prompt': prompt, 'response': response})

    def get(self, request, *args, **kwargs):
        conversations = request.session.get('conversations', [])
        return JsonResponse({'conversations': conversations})


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer