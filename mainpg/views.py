from django.shortcuts import render
from django.views.generic import *

from accounts.models import Alumini
from django.contrib.auth.models import User

# Create your views here.
def home_view(request):
    return render(request, 'mainpg/intro.html')

class TestView(ListView):
    model = Alumini
    context_object_name = 'alumini_list'
    template_name = 'feature/test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['is_admin'] = user.groups.filter(name='admin').exists()
        return context

class SearchView(ListView):
    model = Alumini
    context_object_name = 'alumini_list'
    template_name = 'search/sort.html'
    paginate_by = 5

    def get_queryset(self):
        sort = self.request.GET.get('sort', '-name')  # 기본 정렬 기준은 name
        allowed_fields = ['name', 'th', 'company', 'contact','-name', '-th', '-company', '-contact']  # Alumini 모델의 정렬 가능한 필드

        if sort not in allowed_fields:
            sort = '-name'  # 허용되지 않은 필드는 name으로 fallback

        return Alumini.objects.all().order_by(sort)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort'] = self.request.GET.get('sort', 'name')  # 현재 정렬 기준을 템플릿에 전달
        return context


from django.http import JsonResponse

def hello(request):
    # GET 요청에서 message 파라미터 읽기
    message = request.GET.get("message", "")
    return JsonResponse({"received_message": message, "status": "success"})
