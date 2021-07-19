from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
# views.py 의 위치에서 models.py 를 찾아서 question 을 import 하라는 의미.
from .models import Question
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
# 아래 코드에서 app1 은 있어도 없어도 결과는 같다.
from app1.forms import QuestionForm
# 21.07.19. 페이징 처리 관련 모듈 import
from django.core.paginator import Paginator



def index(request):
    # REQUEST 는 외부 사용자의 요청을 받아오는것
    # render : 템플릿에 로딩할때 사용.
    # redirect : url 로 이동시 사용.
    # 사용자가 localhost:8000/app1 페이지 접속 이라는 요청을 보냈다.
    # view -> urls 에 어떤 함수를 실행 할지를 확인.
    # view 에서 model 단에 요청
    # 요청의 내용 : 조회 (question 테이블/모델 create_date 컬럼을 기준으로
    # 정렬해서 가져옴) -> 그 결과를 question_list 변수에 저장
    # 21.07.09 질문 목록 가져오기.('-' 는 내림차순 정리).

    page = request.GET.get('page', '1')

    question_list = Question.objects.order_by('-create_date')
    # context 라는 변수에 딕셔너리 형태로 question_list key 와 value 를 저장
    # 테플릿단에서 해당 데이터를 쉽게 조회하기 위해.

    # 페이징 처리내용 = 가져온 데이터를 10개씩 보여줘라
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    # 아래 코드에서 question_list <-- page_obj 로 변경하면 게시판 한 페이지에 질무글이 10개씩만 보이게 됨.
    # context = {'question_list': question_list}
    context = {'question_list': page_obj}

    # 받은 요청에 대해 (request)
    return render(request, 'app1/question_list.html', context)

def detail(request, question_id):
    # get_object_or_404 : 기본키에 해당하는 건이 없다면 404 출력.
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'app1/question_detail.html', context)

def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(answer_content=request.POST.get('answer_content'), create_date=timezone.now())
    # redirect : 함수에 전달된 값을 참고해 페이지 이동을 수행하는 함수
    return redirect('app1:detail', question_id=question.id)

# 질문 등록 함수 21.07.13
def question_create(request):
    # 수정내용 : GET, POST(주소에 데이터가 포함/느리다) 방식에 대한 처리
    # question_form 으로 들어올때
    # 질문을 등록할때
    # post 방식인지 get 방식인지 확인
    # 이유 : 단순히 질문등록 페이지를 오픈한 것인지
    # 아니면 질문등록 페이지에 데이터를 입력해서 저장한것인지를 구분
    if request.method == "POST":
        # forms.py 에 설정한 QuestionForm 클래스를 호출
        # request.POST : 사용자가 입력한 데이터를 받아온다.
        form = QuestionForm(request.POST)
        # 변수 form 에 들어온 값이 올바른 값(정상적인 값인지 확인)
        if form.is_valid():
            # 저장을 하기전 잠시 유보.
            # question 변수에 form 에서 받아온 데이터는 넣어 뒸지만
            # 아직 DB 로 저장하지는 않았다
            question = form.save(commit=False)
            # create_date 컬럼을 따로 입력받지않은 이유?
            # 현재시간으로 입력받기 위해 view 에서 처리
            question.create_date = timezone.now()
            # .save 없으면 저장 안되서 에러 발생
            question.save()
            return redirect('app1:index')
            # return render('app1:index') <-- 에러
    else:
        form = QuestionForm()
        context = {'form': form}
    return render(request, 'app1/question_form.html', {'form': form})

# 0714 수정 (기존내용 백업)
# def question_create(request):
#     form = QuestionForm()
#     return render(request, 'app1/question_form.html', {'form': form})




# get 방식과 post 방식(데이터 전송방식)
# get 방식  : URL 에 파라미터를 붙여서 전송하는 방식
#             속도가 빠르다는 장점이 있지만
#             URL 에 데이터를 실어서 보내기 때문에 보안에 취약하거나
#             그외 데이터 전송에 여러가지 제한 사항이 있다.
# post 방식 : HTML 의 BODY 영역에 데이터를 실어 보내는 방식 (form)
#             대용량의 데이터를 보낼수있고 주소에 실어 보내지 않기 때문에
#             get 방식에 비해 보안성 또한 좋다
# csrf_token : 브라우저에서 작성된 데이터가 올바른 데이터인지,
#              혹은 진짜 웹 브라우저에서 작성된 데이터인지 판단하는 기능
#             -디장고의 기본기능


# <!--템플릿 태그-->
# <!--{% if 요청 받은 값(question_list)%} : Question_list 가 있을 경우.-->
# <!--{% for 임시변수 in 요청 받은 값(딕셔너리의 키 값) %} : 딕셔너리 키의 value 를 -->
# <!--    반복하여 순차적으로 임시변수에 대입/-->
# <!--{{ 임시변수.컬럼 }} : for 문에 의해 선언 된 임시변수의 컬럼출력(데이터 표현은 중괄호 2개 임. %% 아님.-->
# {{ }} : 데이터와 관련된 내용을 출력할때 사용하는 템플릿 태그
# {% %} : 템플릿 태그의 속성, 문법 등을 사용할때 쓰는 태그