# Django tuto
> [점프 투 장고](https://wikidocs.net/72377)

## 장고 시작하기
 ```py
    # django 프로젝트 시작하기
    django-admin startproject config .

    # django 앱 시작하기
    django-admin startap <project name>
 ```

## 장고 서버의 원리
 1. 사용자가 django 앱이 실행중인 주소로 접속한다.
 2. django 서버는 `config/urls.py`를 확인해서 사용자가 요청한 주소와 일치하는 주소를 찾는다.
 3. `config/urls.py`는 해당주소에 대응되는 웹페이지 리턴함수를 찾아 반환한다.

## 장고 모델 관리
 ```py
    # 장고 데이터베이스 테이블 생성
    python manage.py migrate
 ```

 * 모델 작성
  - `pybo.models.py`에 pybo앱에서 사용할 모델들을 작성 및 관리할 수 있다.
  - 각 모델들은 필드를 변수로 가질 수 있다. 자세한 필드들은 다음 링크를 확인하면 된다. [Django Model Fields](https://docs.djangoproject.com/en/4.0/ref/models/fields/#field-types)
 
 * 테이블 생성
  - `config/setting.py`에 있는 INSTALLED_APPS 변수에 다음을 추가해준다. `pybo.apps.PyboConfig`
  - 위 작업이 완료되면 테이블 생성 명령어를 입력한다.

  ```py
    # 모델의 생성, 변경 적용 명령어
    python manage.py makemigrations
    # 장고 데이터베이스 테이블 생성
    python manage.py migrate
  ```
 * 모델 사용하기
  ```py
    # 장고 쉘 진입
    python manage.py shell
  ```
  - 위 명령어를 입력하여 장고 쉘에 진입해 데이터베이스 작업이 가능하다.
  - 데이터베이스 쿼리 작업은 다음 링크를 확인하면 된다. [Django Queries](https://docs.djangoproject.com/en/4.0/topics/db/queries/)

## 장고 관리자
 ```py
    # 장고 관리자 계정 생성
    python manage.py createsuperuser
 ```
 * 관리자 사이트에 모델 추가하기
 ```py
    # pybo/admin.py
    # 파이썬 어드민 페이지 추가하기
    from .models import Question
    admin.site.register(Question)
 ```

 * 관리자 사이트에 검색기능 추가하기
 ```py
    # pybo/admin.py
    class QuestionAdmin(admin.ModelAdmin):
    search_fields = [
        'subject',   
    ]
    admin.site.register(Question, QuestionAdmin)
 ```
  - 그 이외 다양한 기능들은 다음 링크를 참고한다. [Django Admin](https://docs.djangoproject.com/en/4.0/ref/contrib/admin/)

## 장고 템플릿
 * 템플릿 디렉토리 설정
  - 템플릿 파일을 저장할 경로를 `config/settings.py`에 입력해줘야 한다.
  ```py
    TEMPLATES = [
        ...
        'DIRS': [ BASE_DIR / 'templates' ]
        ...
    ]
  ```
  - 여기서 `BASE_DIR`는 config가 있는 경로를 의미한다. 따라서 템플릿이 있는 경로는 `./templates/`이다.

  * 템플릿 작성하기
   - 장고 템플릿은 기본적으로 html 문법을 따르고, 추가적으로 파이썬 문법을 사용할 수 있다.
   - `{%  %}`로 감싸인 부분을 템플릿 태그리고 부르며 여기서는 파이썬 명령을 사용할 수 있다.
   - `{{ }}`로 감싸인 부분은 파이썬 변수를 사용할 수 있다.
   - 마지막으로 템플릿 태그는 파이썬 코드처럼 identation이 따로 없으므로 종료 부분을 명시해주어야만 한다.
   - 자세한 부분은 다음 링크를 참고하면 된다. [Django Templates](https://docs.djangoproject.com/en/4.0/topics/templates/)

 * 제네릭 뷰
  - 특정한 패턴이 있는 뷰를 작성할 때 이를 패턴화하여 간략하게 만든 것을 의미한다.
 ```py
    # 제네릭 뷰 미사용
    def index(request):
        question_list = Question.objects.order_by('-create_date')
        context = {
            'question_list': question_list
        }
        return render(request, 'pybo/question_list.html', context=context)

    # 제네릭 부 사용
    class IndexView(generic.ListView):
        def get_queryset(self):
            return Question.objects.order_by('-create_date')
 ```

## URL 별칭
 * URL 별칠
  - url 하드코딩, 즉 url을 쓸 때마다 폴더를 전부 고려해서 작성하다보면, 추후 url 리팩토링 시에 매번 다 수정하는 소요가 발생할 수 있다. 따라서 이를 해결하기 위해 URL 별칭을 사용한다.
  - url 매핑에 name 속성을 부여한다.
  ```py
    # 'pybo/urls.py'
    # url 별칭 이전
    path('', views.index)
    # url 별칭 이후
    path('', views.index, name='index')
  ```

  ```html
    <!-- question_list.html -->
    <!-- url 별칭 이전 -->
    <a href="/pybo{{ question.id }}">
    <!-- url 별칭 이후 -->
    <a href="{% url 'detail' question_id=question.id %}">
  ```

 * 네임스페이스
  - 장고 프로젝트에서 한가지 앱만 사용한다면 문제가 없을 수 있지만, 아니라면 위와 같이 사용하는 것은 문제가 발생할 수 있다. 따라서 네임스페이스를 사용하면 이를 해결할 수 있다.
  - `pybo/urls.py`에 `app_name = "pybo"`를 추가해주면 된다.
  - 네임스페이스를 추가했으므로 템플릿이나 redirect 함수 같은 곳에서도 이를 명시해줘야 한다.
  ```html
    <!-- 네임스페이스 사용 이전 -->
    <a href="{% url 'detail' question_id=question.id %}">
    <!-- 네임스페이스 사용 -->
    <a href="{% url 'pybo:detail' question_id=question.id %}">
  ```

## 데이터 저장
 * 폼
  - POST 형식으로 웹페이지에서 데이터베이스를 조작한다고 생각해보자. 먼저 장고는 `<form>` 태그 바로 밑에 `{% csrf_token %}`이 존재해야지만 POST 요청을 사용할 수 있다. 이는 해당 요청이 자동화 요청인지 실제 사용자의 요청인지를 구별하는 검증 기술이다.
  ```html
    <form action="{% url 'pybo:answer_create' question.id %}" method="post">
        {% csrf_token %}
        <textarea name="content" id="content" rows="15"></textarea>
        <input type="button" value="답변등록">
    </form>
  ```

## 스테틱
 * 스타일시트
  - 스타일시트는 장고 스테틱에 보관해야 한다. 이는 템플릿과 동일하게 `config\settings.py`에 작업을 해야한다.
  ```py
    STATIC_URL = 'static/'
    STATICFILES_DIRS = [
        BASE_DIR / 'static'
    ]
  ```
  - 스타일시트를 html문서가 읽게 하기 위해서는 해당 html문서 최상단에 다음을 추가해야한다.
  ```html
    {% load static %}
    <link rel="stylesheet" type="text/css" href="{% static 'style.css' %}">
  ```
