from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)  # 책 제목
    author = models.CharField(max_length=100)  # 저자
    publish_date = models.DateField()  # 출판일
    isbn = models.CharField(max_length=13, unique=True)  # ISBN
    description = models.TextField()  # 책 설명
    image_url = models.URLField()  # 이미지 URL
    aladin_link = models.URLField()  # aladin 링크

    def __str__(self):
        return self.title
