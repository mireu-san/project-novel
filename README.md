## Welcome!
- 현재 이 프로젝트는 진행중입니다. 문의사항은 메일 또는 DM 부탁드립니다.
- This project supports Korean language at the moment. Please send an email or DM me if you have any question regarding this project.

## 예상 Docker 컨테이너 내부 구조
- (local: Backend/project_novel -> Docker: Backend/app)
/
├── app
│   ├── chatbot
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   │   └─ __init__.py
│   │   ├── models.py
│   │   ├── templates
│   │   │   ├── base.html
│   │   │   └─ chat.html
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └─ __init__.py
│   ├── project_novel
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └─ __init__.py
│   └─ manage.py
└─ tmp

## Crash note
(임시성격이 강한 경우, 구분을 위해 영어로 작성)

### postgresql settings.py
pgadmin 7.3 이 안전한 버전. 7.4 에서 다운그레이드함.


### postgresql 
psql -U <usernamehere!>
<!-- 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dbnovel',
        # must be changed to other username later.
        'USER': 'postgres',
        'PASSWORD': '(rename it once this configuration is reused)',
        'HOST': 'localhost',
        'PORT': '5432',
    }
} -->

### python, virtual environment
- dotenv 가 작동하지 않는 문제. 이는 interpreter 의 문제.
- https://code.visualstudio.com/docs/python/environments#_select-and-activate-an-environment
- 생성 한 가상환경 폴더 내부의 다음 경로로 interpreter 재설정.
`(윈도우 기준 기타 상위폴더 경로들)\backend\venv\Scripts\python.exe`
