from django.urls import path

from . import views

# 'app1' => 아래 name='index'의 별칭
app_name = 'app1'

urlpatterns = [
    path('', views.index, name='index'),
    # --- 상세보기 페이지 추가 21.07.12(king) detail, answer url 부여--------------------
    path('<int:question_id>/', views.detail, name='detail'),
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    # --- 21.07.13 질문등록 url 부여 --------------------------------------------------
    path('question/create', views.question_create, name='question_create'),
    # --- 21.07.21. 퀴즈 : question_modify url 등록. 위에서 형식 참조. 규칙성 있게 만들면 추후 사용 편리성 증대 -------
    path('question/modify/<int:question_id>/', views.question_modify, name='question_modify'),
]

