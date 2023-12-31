## Table of Contents
- [Skills](#skills)
      - [Language and Tool](#language-and-tool)
  - [기술 목표](#기술-목표)
  - [개발 상태](#개발-상태)
  - [특이사항](#특이사항)
  - [Git Convention](#git-convention)
  - [celery 적용 전후 기록](#celery-적용-전후-기록)

![image](./assets/images/cover.jpg)

## 개요
OpenAI 의 API인 ChatGPT 를 해당 웹서비스에 적용하여, 응답 내용에 기반하여 개인의 선호에 근접한 라이트노벨을 추천 하는 챗봇 서비스입니다.

[참고] 아래 workflow image는 예고 없이 변경 될 수 있습니다.

![image](./assets/images/novel-gpt-diagram.jpg)

# Skills
#### Language and Tool

<img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white">
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=white">
<img src="https://img.shields.io/badge/jwt-000000?style=for-the-badge&logo=jwt&logoColor=white">

## 기술 목표
Vite(reactjs)기반의 client 에서, Django 서버 (handling openAI)와 송수신(I/O)을 해서, 개인 맞춤형 서비스. 이 과정에서 User 기능 및 DB에 대화내용을 기록하는 것.

## 개발 상태
1차 개발 완료 후, 고도화 작업 단계입니다.

## API Reference
리팩토링 작업 후, 업데이트 예정입니다.

## ERD
리팩토링 작업 후, 업데이트 예정입니다.

<!-- command sheet - checklist -->
<!-- ```
pip freeze > requirements.txt
chmod +x ./entrypoint.sh
http://0.0.0.0:8000
docker compose up -d --build
./manage.py startapp taskapp
docker exec -it django /bin/sh
``` -->

## TIL / 회고록
업데이트 예정입니다.
- pycurl 을 사용하지 않은 이유.
- [토큰과 소셜 인증 구성 과정 기록 - (1)](https://medium.com/@bellwoan/django-%EC%9D%B8%EC%A6%9D-%EA%B5%AC%EC%84%B1-%EA%B3%BC%EC%A0%95-%EA%B8%B0%EB%A1%9D-c8d2a548b046)

## celery 적용 전후 기록
celery worker 로 적용을 고려할 초기 기획단계에서는, GPT-3 의 성능이 분명하게 응답에 있어 다소 느린 문제가 있었습니다. 그러나 현 celery worker 까지의 적용 및 할당 시점에서는, openAI 의 API 서버 자체적으로 성능이 개선되어 지금은 무겁지 않게 되었습니다.

그럼에도, 기획 단계의 구상대로 구성을 진행하여 비교해 보았습니다.
대상은, response 에 대한 응답입니다.
- celery 적용 전 대비, 적용 이후에는 410m/s 수준으로, 유의미하게 개선되었습니다. (약 50% 성능 향상)
- 테스트 조건 : 'predefined prompt 적용 이 후, 복합적으로 3가지 문항에 맞게 질문'

## Client
https://github.com/mireu-san/lightnovel-gpt-client
