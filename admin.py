from django.contrib import admin

# Register your models here.
from polls.models import Question, Choice

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
   fields = ['question_text', 'pub_date',]
   readonly_fields = ['pub_date',]
   '''
    fieldsets = [
        ('Question Statement', {'fields':['question_text']}),
        ('Date Information', {'fields':['pub_date'], 'classes':['cllapse']}),
    ]
    inlines = [ChoiceInline]                        # Choice 모델 클래스 같이 보기
    list_display = ('question_text', 'pub_date')    # 레코드 리스트 컬럼 지정
    list_filter = ['pub_date']                      # 필터 사이드 바 주가
    search_fields = ['question_text']               # 검색 박스 추가
    '''

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['question', 'choice_text', 'votes']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)