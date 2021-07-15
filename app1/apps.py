from django.apps import AppConfig

# settings.py 에 해당 항목을 추가 시켜야
# app1을 장고가 인식 할 수 있게된다.
# DB 관련작업에 대한 내용.
# 장고는 models.py 를 이용해서 DB테이블을 생성한다
# 모델은 앱에 종속 되어있다.
class App1Config(AppConfig):
    name = 'app1'
