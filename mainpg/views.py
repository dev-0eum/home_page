from django.shortcuts import render
from django.views.generic import *
from django.urls import reverse
from django.http import *
from django.urls import reverse_lazy

from accounts.models import Alumini
from django.contrib.auth.models import User
from mainpg.forms import *
from mainpg.models import News

# Create your views here.
def home_view(request):
    news_list = News.objects.all().order_by('-created_at')[:6]
    return render(request, 'mainpg/intro.html', {'news_list': news_list})

############# Admin #############
class TestView(ListView):
    model = Alumini
    context_object_name = 'alumini_list'
    template_name = 'feature/test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['is_admin'] = user.groups.filter(name='admin').exists()
        return context


############# Search #############
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



############# News #############
class NewsView(ListView):
    model = News
    context_object_name = 'news_list'
    template_name = 'news/feed.html'
    ordering = ['-created_at'] # 최신순 정렬 
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['can_upload'] = user.groups.filter(name='admin').exists()
        return context

class NewsCreateView(CreateView):
    model = News
    context_object_name = 'news'
    form_class = NewsForm
    template_name = 'news/create.html'

    # Form을 임시로 받아서, temp의 정보와 req의 정보가 동일한지 체크
    def form_valid(self, form):
        # temp에 form 임시 저장 
        temp = form.save(commit=False)
        group_names = [group.name for group in self.request.user.groups.all()]
        print(group_names)

        # Admin 그룹권한 확인
        if('admin' in group_names):
            # 실제로 데이터 저장
            temp.save()
            return super().form_valid(form)
        else:
            print("Permission Denied")

    
    # Redirect to URL
    def get_success_url(self):
        return reverse('mainpage:news')
    
########################
class NewsDetailView(DetailView):
    model = News
    context_object_name = 'target_news'
    template_name = 'news/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['is_admin'] = user.groups.filter(name='admin').exists()
        return context

class NewsUpdateView(UpdateView):
    model = News
    form_class = NewsUpdateForm # id가 변경 가능한 폼 >> 그래서 새로운 폼
    context_object_name = 'target_news'
    success_url = reverse_lazy('mainpage:news')
    template_name = 'news/update.html'

    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return super().get(*args,**kwargs)
        else:
            return HttpResponseForbidden()
        
    def post(self,*args,**kwargs):
        if self.request.user.is_authenticated:     #and self.get_object() == self.request.user:
            return super().post(*args,**kwargs)
        else:
            return HttpResponseForbidden()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['is_admin'] = user.groups.filter(name='admin').exists()
        return context

class NewsDeleteView(DeleteView):
    model = News
    context_object_name = 'target_news'
    success_url = reverse_lazy('mainpage:news')
    template_name = 'news/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['is_admin'] = user.groups.filter(name='admin').exists()
        return context

############# DRF API #############
from django.http import JsonResponse

def hello(request):
    # GET 요청에서 message 파라미터 읽기
    message = request.GET.get("message", "")
    return JsonResponse({"received_message": message, "status": "success"})
