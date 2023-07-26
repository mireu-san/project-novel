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
