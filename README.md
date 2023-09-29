# Welcome!

## 프로젝트 주제
바닐라 자바스크립트(client/client) 가 openAI에 바로 송수신을 해서 개인 맞춤형 서비스 제공 및 데이터 수집/분석 구현에 어려움이 있었음. 장고(server/server) 서버를 거쳐서 OpenAI 간의 I/O를 진행. 이 과정에서 User 기능 및 DB에 대화내용을 기록하는 것.

`요약: 유저는 로그인 해서 개인의 대화 기록을 유지하면서 자신의 취향에 맞는 라이트노벨을 찾는데 도움을 제공하는 서비스.`

## 한계
- DB 의 경우 아직 postgresql를 도입하지 않았습니다.
- django 만으로 작동 중 입니다. (nginx 와 같은 reverse proxy, 정적 파일 처리 미적용)
- docker 로 컨테이너화 하지 않았습니다 (이 후, aws ec2에 호스팅).
- UI 보다는 데이터 I/O 가능 여부에 중점을 두고 개발했습니다.
- 법률 관련은 임시로 배제하고 개발했습니다.

<!-- ## 메모. -->
<!-- ### postgresql settings.py
pgadmin 7.3 이 안전한 버전. 7.4 에서 다운그레이드함. -->
<!-- ### postgresql  -->
<!-- psql -U <usernamehere!> -->
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
<!-- https://www.commandprompt.com/education/how-to-rename-a-userrole-in-postgresql/ -->
### 메모
python, virtual environment
- dotenv 가 작동하지 않는 문제. 이는 interpreter 의 문제.
- https://code.visualstudio.com/docs/python/environments#_select-and-activate-an-environment
- 생성 한 가상환경 폴더 내부의 다음 경로로 interpreter 재설정.
`(윈도우 기준 기타 상위폴더 경로들)\backend\venv\Scripts\python.exe`

### nginx, uwsgi (구상)
- Nginx 가 client 에서 모든 http request 를 수신
- 정적이면 Nginx 로, 그러나 장고 앱에 대한 요청이면 uwsgi 서버로 요청.
- uwsgi가 장고 앱을 실행.
`요약: Nginx가 client로부터 모든 http request를 수신하고, 정적 파일이면 Nginx가 처리하고, 그 외의 경우 uwsgi 서버로 요청을 전달하는 구성을 계획중.`


### users/serializers.py - create (암호화)
https://stackoverflow.com/questions/50797170/password-encryption-in-django-using-serializerdrf

- 비밀번호 암호화 부분입니다. 
- make_password 를 이용해서, 비밀번호를 해쉬 처리 함으로서 암호화가 됩니다.
```
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super(UserSerializer, self).create(validated_data)
        user.password = make_password(password)
        user.save()
        return user
```



### Django Rest Framework page
http://localhost:8000/chatbot/api/conversation/

### Crash note:
![이미지 설명](/image/a1.jpg)
![이미지 설명](/image/a2.jpg)


(※참고: 더는 작동하지 않는 instance 및 DB.)

1. aws lightsail
  - httpd (apache)
  - nginx 와의 포트넘버 충돌 및 우회
  - 쓰기/읽기 권한 부여 (uwsgi)

- 잘못된 접근
  - server 실행 후, 클라이언트 쪽 index.html 을 계속 실행하려 함.

### 피드백
- 개발용은 일단 로컬 상에서 협업 하더라도, 서로 먼저 테스트를 해 보고 나서 견본 수준으로 완성이 되고 나면 이를 토대로 cloud 서버에서 별도로 git clone 후 설정 및 테스트 작업을 위한 준비를 하는 것.
- 현 진행중인 프로젝트 계획의 개요 정도는 개인적으로라도 kanban 같은 곳에 기록 해 두는게 도움이 됨.
- 유사 구현 사례를 좀 더 다양하게 찾아 볼 필요성.

2. client와 server 간의 I/O
![이미지 설명](/image/b1.jpg)
![이미지 설명](/image/b2.jpg)
![이미지 설명](/image/b3.jpg)
```
main.js:11 console.trace
window.onbeforeunload @ main.js:11
Navigated to http://127.0.0.1:5500/client/index.html
main.js:16 Imports successful.
main.js:28 Initial data: [{…}]
main.js:41 Data after push: (3) [{…}, {…}, {…}]
main.js:46 Initial questionData: []
main.js:51 Inputs: NodeList(3) [input#input1, input#input2, input#input3]
main.js:76 Form submitted.
main.js:83 Inputs after replacement: 이것은 실험용 메세지입니다 알겠죠?
main.js:88 Combined question: 이것은. 실험용. 메세지입니다 알겠죠?.
main.js:95 Inputs after reset:   
main.js:70 Question sent: 이것은. 실험용. 메세지입니다 알겠죠?.
main.js:104 API call start
api.js:21 API 요청 처리 시간: 3431 ms
main.js:106 API call finished
main.js:107 장고 서버에서, prompt, response 를 처음 수신하는 곳 {prompt: '이것은. 실험용. 메세지입니다 알겠죠?.', response: '알겠습니다. 실험용 메세지를 이해했습니다.'}
main.js:109 Before printAnswer call
ui.js:28 printAnswer called with answer: 알겠습니다. 실험용 메세지를 이해했습니다.
ui.js:31 답변 수신 전까지 출력 할, 입력했던 내용: <li class="question"><span>다음의 문장을 기반으로 알아보고 있어요: </span><span>이것은. 실험용. 메세지입니다 알겠죠?.</span></li>
ui.js:39 li: <li class=​"answer fade">​…​</li>​
ui.js:43 django server 로 부터, openAI의 response 를 client 에서 수신 받은 내용: <li class="answer fade">알겠습니다. 실험용 메세지를 이해했습니다.</li>
ui.js:66 copyButton <button class=​"copyButton" type=​"button">​이 답변 내용을 복사합니다.​</button>​
ui.js:75 link: a#copyButton2
ui.js:87 resetButton: button.resetButton
main.js:111 After printAnswer call
main.js:125 questionData after reset: []
main.js:127 $chatList: ul
 console.trace
window.onbeforeunload @ main.js:11
socket.onmessage @ index.html:89
Navigated to http://127.0.0.1:5500/client/index.html
main.js:16 Imports successful.
main.js:28 Initial data: [{…}]
main.js:41 Data after push: (3) [{…}, {…}, {…}]
main.js:46 Initial questionData: []
main.js:51 Inputs: NodeList(3) [input#input1, input#input2, input#input3]
```

### 그 외 기능.
- DB에 대화 내역이 저장되고 있습니다.
![이미지 설명](/image/c1.jpg)
- prompt 와 response 값 설정을 통한 테스트.
![이미지 설명](/image/c2.jpg)

### 로그인 기능.
```
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
```
```
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super(UserSerializer, self).create(validated_data)
        user.password = make_password(password)
        user.save()
        return user
```
```
document.addEventListener('DOMContentLoaded', () => {
    const loginButton = document.getElementById('login-btn');
    const loginForm = document.getElementById('login-form');
    const submitLoginFormButton = document.getElementById('submit-login-btn');

    loginButton.addEventListener('click', () => {
        loginForm.style.display = 'block';
    });

    submitLoginFormButton.addEventListener('click', (e) => {
        e.preventDefault();

        const username = loginForm.querySelector('input[name="username"]').value;
        const password = loginForm.querySelector('input[name="password"]').value;

        axios.post('http://localhost:8000/api/token/', {
            username: username,
            password: password
        }).then(response => {
            console.log(response.data);
        }).catch(error => {
            console.log(error);
        });
    });
});

```
![이미지 설명](/image/login1.jpg)
```
login.js:20 
{refresh: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90e…iOjJ9.2sr8Z8Ocw79zrKb7QpqgVn7kigtP0tH0luQJk64IqSE', access: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90e…I6Mn0.svDR-FE_wbun81IWMi3D4kfPkbBludIZz80IiKQpOrs'}
access
: 
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkwOTkyMjU1LCJpYXQiOjE2OTA5OTE5NTUsImp0aSI6IjE2ZGQxMDMwNmYwYjQ1NGU5Y2VmNGIwNDAxOWVkMzA3IiwidXNlcl9pZCI6Mn0.svDR-FE_wbun81IWMi3D4kfPkbBludIZz80IiKQpOrs"
refresh
: 
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5MTA3ODM1NSwiaWF0IjoxNjkwOTkxOTU1LCJqdGkiOiIyMWE5NTcxMGIwNWM0NzRjYTdjZDMwZmExMzNmMGM0OSIsInVzZXJfaWQiOjJ9.2sr8Z8Ocw79zrKb7QpqgVn7kigtP0tH0luQJk64IqSE"
[[Prototype]]
: 
Object
```

![이미지 설명](/image/d1.jpg)


```
projectLightNovel-main
├─ .gitignore
├─ backend
│  └─ project_novel
│     ├─ .dockerignore
│     ├─ .gitignore
│     ├─ chatbot
│     │  ├─ admin.py
│     │  ├─ apps.py
│     │  ├─ migrations
│     │  │  ├─ 0001_initial.py
│     │  │  └─ __init__.py
│     │  ├─ models.py
│     │  ├─ serializers.py
│     │  ├─ templates
│     │  │  ├─ base.html
│     │  │  └─ chat.html
│     │  ├─ tests.py
│     │  ├─ urls.py
│     │  ├─ views.py
│     │  └─ __init__.py
│     ├─ chat_history
│     │  └─ migrations
│     ├─ core
│     │  ├─ asgi.py
│     │  ├─ settings.py
│     │  ├─ urls.py
│     │  ├─ wsgi.py
│     │  └─ __init__.py
│     ├─ docker-compose.yml
│     ├─ Dockerfile
│     ├─ manage.py
│     ├─ nginx
│     │  └─ nginx.conf
│     ├─ requirements.txt
│     ├─ staticfiles
│     │  ├─ admin
│     │  │  ├─ css
│     │  │  │  ├─ autocomplete.css
│     │  │  │  ├─ base.css
│     │  │  │  ├─ changelists.css
│     │  │  │  ├─ dark_mode.css
│     │  │  │  ├─ dashboard.css
│     │  │  │  ├─ forms.css
│     │  │  │  ├─ login.css
│     │  │  │  ├─ nav_sidebar.css
│     │  │  │  ├─ responsive.css
│     │  │  │  ├─ responsive_rtl.css
│     │  │  │  ├─ rtl.css
│     │  │  │  ├─ vendor
│     │  │  │  │  └─ select2
│     │  │  │  │     ├─ LICENSE-SELECT2.md
│     │  │  │  │     ├─ select2.css
│     │  │  │  │     └─ select2.min.css
│     │  │  │  └─ widgets.css
│     │  │  ├─ img
│     │  │  │  ├─ calendar-icons.svg
│     │  │  │  ├─ gis
│     │  │  │  │  ├─ move_vertex_off.svg
│     │  │  │  │  └─ move_vertex_on.svg
│     │  │  │  ├─ icon-addlink.svg
│     │  │  │  ├─ icon-alert.svg
│     │  │  │  ├─ icon-calendar.svg
│     │  │  │  ├─ icon-changelink.svg
│     │  │  │  ├─ icon-clock.svg
│     │  │  │  ├─ icon-deletelink.svg
│     │  │  │  ├─ icon-no.svg
│     │  │  │  ├─ icon-unknown-alt.svg
│     │  │  │  ├─ icon-unknown.svg
│     │  │  │  ├─ icon-viewlink.svg
│     │  │  │  ├─ icon-yes.svg
│     │  │  │  ├─ inline-delete.svg
│     │  │  │  ├─ LICENSE
│     │  │  │  ├─ README.txt
│     │  │  │  ├─ search.svg
│     │  │  │  ├─ selector-icons.svg
│     │  │  │  ├─ sorting-icons.svg
│     │  │  │  ├─ tooltag-add.svg
│     │  │  │  └─ tooltag-arrowright.svg
│     │  │  └─ js
│     │  │     ├─ actions.js
│     │  │     ├─ admin
│     │  │     │  ├─ DateTimeShortcuts.js
│     │  │     │  └─ RelatedObjectLookups.js
│     │  │     ├─ autocomplete.js
│     │  │     ├─ calendar.js
│     │  │     ├─ cancel.js
│     │  │     ├─ change_form.js
│     │  │     ├─ collapse.js
│     │  │     ├─ core.js
│     │  │     ├─ filters.js
│     │  │     ├─ inlines.js
│     │  │     ├─ jquery.init.js
│     │  │     ├─ nav_sidebar.js
│     │  │     ├─ popup_response.js
│     │  │     ├─ prepopulate.js
│     │  │     ├─ prepopulate_init.js
│     │  │     ├─ SelectBox.js
│     │  │     ├─ SelectFilter2.js
│     │  │     ├─ theme.js
│     │  │     ├─ urlify.js
│     │  │     └─ vendor
│     │  │        ├─ jquery
│     │  │        │  ├─ jquery.js
│     │  │        │  ├─ jquery.min.js
│     │  │        │  └─ LICENSE.txt
│     │  │        ├─ select2
│     │  │        │  ├─ i18n
│     │  │        │  │  ├─ af.js
│     │  │        │  │  ├─ ar.js
│     │  │        │  │  ├─ az.js
│     │  │        │  │  ├─ bg.js
│     │  │        │  │  ├─ bn.js
│     │  │        │  │  ├─ bs.js
│     │  │        │  │  ├─ ca.js
│     │  │        │  │  ├─ cs.js
│     │  │        │  │  ├─ da.js
│     │  │        │  │  ├─ de.js
│     │  │        │  │  ├─ dsb.js
│     │  │        │  │  ├─ el.js
│     │  │        │  │  ├─ en.js
│     │  │        │  │  ├─ es.js
│     │  │        │  │  ├─ et.js
│     │  │        │  │  ├─ eu.js
│     │  │        │  │  ├─ fa.js
│     │  │        │  │  ├─ fi.js
│     │  │        │  │  ├─ fr.js
│     │  │        │  │  ├─ gl.js
│     │  │        │  │  ├─ he.js
│     │  │        │  │  ├─ hi.js
│     │  │        │  │  ├─ hr.js
│     │  │        │  │  ├─ hsb.js
│     │  │        │  │  ├─ hu.js
│     │  │        │  │  ├─ hy.js
│     │  │        │  │  ├─ id.js
│     │  │        │  │  ├─ is.js
│     │  │        │  │  ├─ it.js
│     │  │        │  │  ├─ ja.js
│     │  │        │  │  ├─ ka.js
│     │  │        │  │  ├─ km.js
│     │  │        │  │  ├─ ko.js
│     │  │        │  │  ├─ lt.js
│     │  │        │  │  ├─ lv.js
│     │  │        │  │  ├─ mk.js
│     │  │        │  │  ├─ ms.js
│     │  │        │  │  ├─ nb.js
│     │  │        │  │  ├─ ne.js
│     │  │        │  │  ├─ nl.js
│     │  │        │  │  ├─ pl.js
│     │  │        │  │  ├─ ps.js
│     │  │        │  │  ├─ pt-BR.js
│     │  │        │  │  ├─ pt.js
│     │  │        │  │  ├─ ro.js
│     │  │        │  │  ├─ ru.js
│     │  │        │  │  ├─ sk.js
│     │  │        │  │  ├─ sl.js
│     │  │        │  │  ├─ sq.js
│     │  │        │  │  ├─ sr-Cyrl.js
│     │  │        │  │  ├─ sr.js
│     │  │        │  │  ├─ sv.js
│     │  │        │  │  ├─ th.js
│     │  │        │  │  ├─ tk.js
│     │  │        │  │  ├─ tr.js
│     │  │        │  │  ├─ uk.js
│     │  │        │  │  ├─ vi.js
│     │  │        │  │  ├─ zh-CN.js
│     │  │        │  │  └─ zh-TW.js
│     │  │        │  ├─ LICENSE.md
│     │  │        │  ├─ select2.full.js
│     │  │        │  └─ select2.full.min.js
│     │  │        └─ xregexp
│     │  │           ├─ LICENSE.txt
│     │  │           ├─ xregexp.js
│     │  │           └─ xregexp.min.js
│     │  └─ rest_framework
│     │     ├─ css
│     │     │  ├─ bootstrap-theme.min.css
│     │     │  ├─ bootstrap-theme.min.css.map
│     │     │  ├─ bootstrap-tweaks.css
│     │     │  ├─ bootstrap.min.css
│     │     │  ├─ bootstrap.min.css.map
│     │     │  ├─ default.css
│     │     │  ├─ font-awesome-4.0.3.css
│     │     │  └─ prettify.css
│     │     ├─ docs
│     │     │  ├─ css
│     │     │  │  ├─ base.css
│     │     │  │  ├─ highlight.css
│     │     │  │  └─ jquery.json-view.min.css
│     │     │  ├─ img
│     │     │  │  ├─ favicon.ico
│     │     │  │  └─ grid.png
│     │     │  └─ js
│     │     │     ├─ api.js
│     │     │     ├─ highlight.pack.js
│     │     │     └─ jquery.json-view.min.js
│     │     ├─ fonts
│     │     │  ├─ fontawesome-webfont.eot
│     │     │  ├─ fontawesome-webfont.svg
│     │     │  ├─ fontawesome-webfont.ttf
│     │     │  ├─ fontawesome-webfont.woff
│     │     │  ├─ glyphicons-halflings-regular.eot
│     │     │  ├─ glyphicons-halflings-regular.svg
│     │     │  ├─ glyphicons-halflings-regular.ttf
│     │     │  ├─ glyphicons-halflings-regular.woff
│     │     │  └─ glyphicons-halflings-regular.woff2
│     │     ├─ img
│     │     │  ├─ glyphicons-halflings-white.png
│     │     │  ├─ glyphicons-halflings.png
│     │     │  └─ grid.png
│     │     └─ js
│     │        ├─ ajax-form.js
│     │        ├─ bootstrap.min.js
│     │        ├─ coreapi-0.1.1.js
│     │        ├─ csrf.js
│     │        ├─ default.js
│     │        ├─ jquery-3.5.1.min.js
│     │        └─ prettify-min.js
│     └─ users
│        ├─ admin.py
│        ├─ apps.py
│        ├─ migrations
│        │  ├─ 0001_initial.py
│        │  ├─ 0002_alter_user_email.py
│        │  └─ __init__.py
│        ├─ models.py
│        ├─ serializers.py
│        ├─ tests.py
│        ├─ urls.py
│        ├─ views.py
│        └─ __init__.py
├─ image
│  ├─ a1.jpg
│  ├─ a2.jpg
│  ├─ b1.jpg
│  ├─ b2.jpg
│  ├─ b3.jpg
│  ├─ c1.jpg
│  ├─ c2.jpg
│  ├─ d1.jpg
│  └─ login1.jpg
└─ README.md

```