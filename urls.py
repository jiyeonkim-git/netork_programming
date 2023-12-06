from django.urls import path                    # path 모듈 import
from . import views
from django.views.generic import TemplateView
# 현재 폴더에 views 모듈 import


app_name = 'polls'

urlpatterns = [
    path('', views.index, name='index'),                                                                 # /polls/
    path('<int:question_id>/', views.detail, name='detail'),                               # /polls/1/
    path('<int:question_id>/results/', views.results, name='results'),              # /polls/1/results/
    path('<int:question_id>/vote/', views.vote, name='vote'),                          # /polls/1/vote/
    path('./template-extends/', TemplateView.as_view(template_name='polls/child_template.html')),
    path('form-class-ex/', views.form_class_ex),
    path('form-class-ex-thanks/', TemplateView.as_view(template_name='polls/form_class_ex_thanks.html')),
    path('form-class-ex2/', views.MyFormView.as_view()),
    path('form-class-ex3/', views.MyFormView2.as_view()),
]