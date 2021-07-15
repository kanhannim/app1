from django.contrib import admin

# Register your models here.
# 21.07.08 Question 테이블 (모델) 관리자 페이지에 추가
from .models import Question

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']

admin.site.register(Question, QuestionAdmin)