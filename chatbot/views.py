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
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import logging
from prompt_parser.tasks import process_openai_request
from celery.result import AsyncResult

logger = logging.getLogger("django")

load_dotenv()

# API KEY 를 환경변수로부터 불러옵니다.
openai.api_key = os.getenv("OPENAI_API_KEY")

# 최종 단계에서 활성화 및 구성 예정
# https://platform.openai.com/docs/libraries/python-library
# chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world"}])


@method_decorator(csrf_exempt, name="dispatch")
# 유저가 장고 서버를 통해 interatcion 하도록.


class TaskResultView(APIView):
    def get(self, request, task_id, *args, **kwargs):
        result = AsyncResult(task_id)
        if result.ready():
            # The task has finished, return the result
            return JsonResponse({"status": "SUCCESS", "result": result.result})
        else:
            # The task is not ready, indicate that the client should continue polling
            return JsonResponse({"status": "PENDING"})


class ChatbotView(APIView):
    """
    사용자와 대화하는 챗봇 뷰입니다.

    사용자의 메시지를 받아 OpenAI GPT로부터 응답을 생성하고 반환합니다.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logger.info("Post method entered")

        raw_body = request.body.decode("utf-8")
        print("Received request body:", raw_body)

        user_message = raw_body.strip()

        if not user_message:
            return Response({"error": "Empty message received"}, status=400)

        # Dispatch the OpenAI API call to a Celery task
        task = process_openai_request.apply_async(args=[user_message])
        task_id = task.id  # You can store this task_id to check the status later

        # Optional: Save the task_id to the database or session if needed for later reference.

        return JsonResponse({"task_id": task_id})  # Return task_id to the client

    def get(self, request, *args, **kwargs):
        """
        사용자의 대화 이력을 반환합니다.
        """
        conversations = request.session.get("conversations", [])
        return JsonResponse({"conversations": conversations})


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
            conversation = Conversation.objects.get(pk=pk)  # 특정 대화 조회
            serializer = ConversationSerializer(conversation)
            return JsonResponse(serializer.data)
        else:
            conversations = Conversation.objects.all()  # 전체 대화 목록 조회
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
            serializer.save()  # 데이터가 유효하면 저장
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)  # 유효하지 않으면 오류 반환

    def delete(self, request, pk, *args, **kwargs):
        """
        특정 대화 내역을 데이터베이스에서 삭제합니다.
        """
        # 특정 대화(pk)를 삭제합니다.
        conversation = Conversation.objects.get(pk=pk)
        conversation.delete()  # 대화 삭제
        return JsonResponse(
            {"message": "Deleted successfully"}, status=204
        )  # 성공 메시지 반환
