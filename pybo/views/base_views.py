from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from pybo.models import Question

def index(request):
    page = request.GET.get('page', '1') # http://localhost:8000/pybo/?page=1, page 값이 없을 때는 자동으로 1을 위치함
    kw = request.GET.get('kw', '') # 검색어
    question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) | # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(auther__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__auther__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct() # 중복 값 제거
    paginator = Paginator(question_list, 10) # 페이지 당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    last_page = len(paginator.page_range)
    context = {
        'question_list': page_obj,
        'last_page': last_page,
        'page': page,
        'kw': kw
    }
    return render(request, 'pybo/question_list.html', context=context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {
        'question': question
    }
    return render(request, 'pybo/question_detail.html', context=context)
