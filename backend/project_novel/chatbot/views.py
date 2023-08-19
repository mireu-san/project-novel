# ★chatbot/views.py
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import openai
import os
import json
# from .models import Conversation
from rest_framework import viewsets
# from .serializers import ConversationSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework.authentication import TokenAuthentication, JWTAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from chat_history.models import ChatHistory
from rest_framework import status

# API key를 로드
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


# @method_decorator(csrf_exempt, name='dispatch')
# # 유저가 장고 서버를 통해 interatcion 하도록.
class ChatbotView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_input = request.data[0]['content']
        if not user_input:
            return Response({"detail": "Message is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # OpenAI로부터의 응답 받기
        response = openai.Completion.create(engine="text-davinci-003", prompt=user_input, max_tokens=150)
        openai_response = response.choices[0].text.strip()

        # 응답을 ChatHistory 모델에 저장
        ChatHistory.objects.create(
            user=request.user,
            prompt=user_input,
            response=openai_response
        )
        
        return Response({"response": openai_response}, status=status.HTTP_200_OK)

    # def get(self, request, *args, **kwargs):
    #     conversations = request.session.get('conversations', [])
    #     return JsonResponse({'conversations': conversations})
# DB 내 대화 데이터와 interacting 하도록 (하는 API). 즉, admin, user 모두 DB에 저장된 chat history 관리가능케 하는 API.
# 각 endpoint 에 대한 CRUD 작업을 수행하는 API. (기존 viewsets.ModelViewSet 을 View 로 통일화 및 대체)



# class ConversationView(View):
#     def get(self, request, pk=None, *args, **kwargs):
#         # 특정 대화(pk)를 조회하거나 전체 대화 목록을 반환합니다.
#         if pk:
#             conversation = Conversation.objects.get(pk=pk) # 특정 대화 조회
#             serializer = ConversationSerializer(conversation)
#             return JsonResponse(serializer.data)
#         else:
#             conversations = Conversation.objects.all() # 전체 대화 목록 조회
#             serializer = ConversationSerializer(conversations, many=True)
#             return JsonResponse(serializer.data, safe=False)

#     def post(self, request, *args, **kwargs):
#         # 새로운 대화를 생성합니다.
#         data = json.loads(request.body)
#         serializer = ConversationSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save() # 데이터가 유효하면 저장
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400) # 유효하지 않으면 오류 반환

#     def delete(self, request, pk, *args, **kwargs):
#         # 특정 대화(pk)를 삭제합니다.
#         conversation = Conversation.objects.get(pk=pk)
#         conversation.delete() # 대화 삭제
#         return JsonResponse({'message': 'Deleted successfully'}, status=204) # 성공 메시지 반환
