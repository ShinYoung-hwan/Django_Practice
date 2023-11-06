from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from pybo.models import Question

def index(request):
    page = request.GET.get('page', '1') # http://localhost:8000/pybo/?page=1, page 값이 없을 때는 자동으로 1을 위치함
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10) # 페이지 당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    last_page = len(paginator.page_range)
    print(last_page)
    context = {
        'question_list': page_obj,
        'last_page': last_page
    }
    return render(request, 'pybo/question_list.html', context=context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {
        'question': question
    }
    return render(request, 'pybo/question_detail.html', context=context)
