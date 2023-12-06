from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import View, FormView
from django.urls import reverse
from polls.models import Question, Choice
from .forms import NameForms, MyForm
from django import forms
# Create your views here.

class MyFormView(View):
    form_class = NameForms
    initial = {'favorite_name': 'Sherlock'}
    template_name = 'polls/form_class_ex.html'

    # GET요청 받았을 경우,
    # 즉 처음 해당 URL로 접속할 때,
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        context = {'form': form}
        return render(request, self.template_name, context)

    # POST요청 받았을 경우,
    # 즉, POST데이터를 받았을 경우,
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_name = form.cleaned_data['favorite_name']
            print('new_name = ', new_name)

            return HttpResponseRedirect('polls/form-class-ex-thanks/')

        # request.POST의 데이터가 유효하지 않으면
        return render(request, self.template_name, {'form': form})

class NameForm(forms.Form):
    favorite_name = forms.CharField(label='Favorite Name', max_length=100)

class MyFormView2(FormView):
    form_class = NameForms
    initial = {'favorite_name': 'Homes'}
    template_name = 'polls/form_class_ex.html'
    success_url = 'polls/form-class-ex-thanks'

    def form_valid(self, form):
        new_name = form.cleaned_data['favorite_name']
        print('new_name_of_MyFormView2 = ', new_name)

        return super(MyFormView2, self).form_valid(form)

def form_class_ex(request):
    if request.method == 'POST':
        form = NameForm(request.POST)

        if form.is_valid():
            new_name = form.cleaned_data['favorite_name']
            print('new_name = ', new_name)
            return HttpResponseRedirect('/polls/form-class-ex-thanks/')
    else:
        form = NameForm()
        context = {'form': form}

    return render(request, 'polls/form_class_ex.html', context)

class MyView(View):
    form_class = MyForm
    initial = {'key':'value'}
    template_name = 'form_template.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # cleaned_data로 관련 로직 처리
            return HttpResponseRedirect('/success')
        return render(request, self.template_name, {'form':form})

def index(request):
    latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
    context = {'latest_question_list':latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question' : question})

def vote(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    try:
        selected_choice = question.choice_set.get(id=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # 설문 투표 폼을 다시 보여준다.
        context = {'question': question, 'error_message': "U didn't select a choice"}
        return render(request, 'polls/detail.html', context)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # POST 데이터를 정상적으로 처리했으면,
        # 그 결과를 보여줄 수 있는 페이지로 이동시키기 위해
        # HttpResponseRedirect 객체를 리턴하는 것이 일반적
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question':question})

def name(request, data=None):
    if request.method == 'POST':
        #form = NameForm(request.POST)
        form = NameForm(data)

        if form.is_valid(): # 폼에 담긴 데이터가 유효한지 체크
           new_name = form.cleaned_data['name']
           return HttpResponseRedirect('')
    else:
        form = NameForm()

    return render(request,'polls/name.html',{'form':form})