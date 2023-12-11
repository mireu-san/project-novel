import os
from celery import shared_task
from .models import Book
import requests
from django.utils.dateparse import parse_date

ALADIN_API_KEY = os.getenv("ALADIN_API_KEY")


@shared_task
def fetch_and_update_books():
    # Aladin OpenAPI에서 데이터를 가져오는 로직
    response = requests.get(
        "http://www.aladin.co.kr/ttb/api/ItemSearch.aspx",
        params={
            "ttbkey": ALADIN_API_KEY,
            "Query": "QUERY",  # 검색할 쿼리
            "QueryType": "Title",  # 검색 유형
            "MaxResults": 10,  # 최대 결과 수
            "start": 1,  # 시작 페이지
            "SearchTarget": "Book",  # 검색 대상
            "output": "json",  # 출력 형식
            "Version": "20131101",  # API 버전
        },
    )
    books_data = response.json()

    # 수집한 데이터를 Django 모델에 저장
    for book_data in books_data["items"]:
        # 날짜 형식 변환
        publish_date = (
            parse_date(book_data["pubdate"]) if "pubdate" in book_data else None
        )

        # Book 모델 업데이트 또는 생성
        Book.objects.update_or_create(
            isbn=book_data.get("isbn13"),
            defaults={
                "title": book_data.get("title"),
                "author": book_data.get("author"),
                "publish_date": publish_date,
                "description": book_data.get("description"),
                "image_url": book_data.get("cover"),
                "aladin_link": book_data.get("link"),
            },
        )
