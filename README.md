# Welcome!

## 프로젝트 주제
Vite(reactjs)기반의 client 에서, Django 서버 (handling openAI)와 송수신(I/O)을 해서, 개인 맞춤형 서비스. 이 과정에서 User 기능 및 DB에 대화내용을 기록하는 것.

`요약: 유저는 로그인 해서 개인의 대화 기록을 유지하면서 자신의 취향에 맞는 라이트노벨을 찾는데 도움을 제공하는 서비스.`

## 개발 상태
현재 개발 중인 프로젝트 입니다. 자세한 사항은 이메일 및 연락처로 문의 바랍니다.

## 특이사항
- django-static.sh
도커 이미지 내부에서 실행하지 않고, 외부에서 이미지 빌드 후 실행 하도록 별도의 스크립트 작성.
[Unix-based system - shebang (#!/bin/sh)]
- middleware/logging_latency.py 생성. 현재 콘솔 내 로그는 별도로 저장하도록 조정 하지않음.

## Git Convention
```
feat – a new feature is introduced with the changes
fix – a bug fix has occurred
chore – changes that do not relate to a fix or feature and don't modify src or test files (for example updating dependencies)
refactor – refactored code that neither fixes a bug nor adds a feature
docs – updates to documentation such as a the README or other markdown files
style – changes that do not affect the meaning of the code, likely related to code formatting such as white-space, missing semi-colons, and so on.
test – including new or correcting previous tests
perf – performance improvements
ci – continuous integration related
build – changes that affect the build system or external dependencies
revert – reverts a previous commit

Source: https://www.freecodecamp.org/news/how-to-write-better-git-commit-messages/
```

<!-- command sheet - checklist -->
<!-- ```
pip freeze > requirements.txt
chmod +x ./entrypoint.sh
http://0.0.0.0:8000
docker compose up -d --build
./manage.py startapp taskapp
docker exec -it django /bin/sh
``` -->

## Before & after - applying celery worker with redis
celery worker 로 적용을 고려할 초기 기획단계에서는, GPT-3 의 성능이 분명하게 응답에 있어 다소 느린 문제가 있었습니다. 그러나 현 celery worker 까지의 적용 및 할당 시점에서는, openAI 의 API 서버 자체적으로 성능이 개선되어 지금은 무겁지 않게 되었습니다.

그럼에도, 기획 단계의 구상대로 구성을 진행하여 비교해 보았습니다.
대상은, response 에 대한 응답입니다.
- celery worker 적용 전(before) : 1.69 seconds
- celery worker 적용 후(after) : 1.49 seconds

거의 무의미한 수준의 미미한 속도 개선을 알 수 있었으나, 분명 반응 속도에 긍정적인 것은 확실하다는 것을 알 수 있었습니다.

## 향후 일정 -->
```
1. 계정 생성 후, chatgpt 처럼 좌측에 기록 열람 및, 삭제 가능하도록. 로그인 기능까지. jwttoken 외 다른 선택지는 없는지.
2. CI/CD. TDD 구동 후, merge to main 으로. 단, merge pull request 거친 후 진행토록.
3. README 개선 필요. EDR 등, work flow 추가 고려.
```

<!-- 
### CI/CD script - redis, celery worker 추가 고려.
```
name: Update Container - main/project-novel
on:
  push:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      db:
        image: postgres:16.0
        env:
          POSTGRES_DB: ${{ secrets.DB_NAME }}
          POSTGRES_USER: ${{ secrets.DB_USER }}
          POSTGRES_PASSWORD: ${{ secrets.DB_PASSWORD }}
        ports:
          - 5432:5432
        options: --health-cmd pg_isready --health-interval 10s --health-timeout 5s --health-retries 5

    env:
      SECRET_KEY: ${{ secrets.SECRET_KEY }}
      DJANGO_DEBUG: ${{ secrets.DJANGO_DEBUG }}
      DB_HOST: localhost
      DB_PORT: 5432
      DB_NAME: ${{ secrets.DB_NAME }}
      DB_USER: ${{ secrets.DB_USER }}
      DB_PASSWORD: ${{ secrets.DB_PASSWORD }}

    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11.5
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Make migrations
        run: |
          python manage.py makemigrations
      
      - name: Apply database migrations
        run: python manage.py migrate

      - name: Run tests
        run: python manage.py test
``` -->