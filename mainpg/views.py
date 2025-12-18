from django.shortcuts import render
from django.views.generic import *
from django.urls import reverse
from django.http import *
from django.urls import reverse_lazy

from accounts.models import Alumini
from django.contrib.auth.models import User
from mainpg.forms import *
from mainpg.models import News, OrgImg

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
        # to check Permission(can_view)
        user = self.request.user
        context['can_view'] = user.groups.filter(name='search').exists()

        context['sort'] = self.request.GET.get('sort', 'name')  # 현재 정렬 기준을 템플릿에 전달
        return context

############# QNA #############
class QNAView(ListView):
    model = Category
    context_object_name = 'target_category'
    template_name = 'coffee-chat/qna.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     news_list = News.objects.all().order_by('-created_at')[:10]
    #     context['news_list'] = news_list
    #     return context

from django.shortcuts import get_object_or_404
class FeedView(ListView):
    model = Question
    context_object_name = 'feed_list'
    template_name = 'coffee-chat/category_feed.html'

    # 1. URL의 category_id에 맞는 글만 필터링해서 보여줌
    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return Question.objects.filter(category_id=category_id).order_by('-created_at')

    # 2. 템플릿 상단에 "학업 Feed"라고 띄우기 위해 카테고리 정보 전달
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # URL에 있는 category_id를 가져옴
        category_id = self.kwargs.get('category_id')
        
        # DB에서 해당 id의 Category 객체를 가져와서 context에 'target_category'로 저장
        # get_object_or_404를 쓰면 없는 카테고리 접속 시 404 에러를 띄워줘서 안전함
        context['target_category'] = get_object_or_404(Category, id=category_id)
        
        return context

class AttiDetailView(TemplateView):
    template_name = 'coffee-chat/atti_detail.html'

class ExpView(TemplateView):
    template_name = 'coffee-chat/exp_feed.html'

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


############# Organization ################
class OrgView(TemplateView):
    model = OrgImg
    context_object_name = 'target_img'
    template_name = 'organization/page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['org_img'] = OrgImg.objects.all().order_by('-created_at')
        return context



class OrgCreateView(CreateView):
    model = OrgImg
    context_object_name = 'org_img'
    form_class = OrgForm
    template_name = 'organization/create.html'

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
        return reverse('mainpage:org')
    
class OrgDeleteView(DeleteView):
    model = OrgImg
    context_object_name = 'target_org'
    success_url = reverse_lazy('mainpage:org')
    template_name = 'organization/delete.html'

    ####### 핵심: URL의 PK 대신 로직으로 삭제할 객체를 지정 #######
    def get_object(self, queryset=None):
        # 1. 가장 최근에 생성된 객체를 가져옴
        obj = OrgImg.objects.order_by('-created_at').first()
        
        # 2. 만약 지울 데이터가 하나도 없다면 404 에러 발생 또는 예외 처리
        if obj is None:
            raise Http404("삭제할 이미지가 없습니다.")
            
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # current user
        user = self.request.user
        # is admin?
        context['is_admin'] = user.groups.filter(name='admin').exists()
        return context
    
############# Question #############
from django.contrib import messages # 메시지 모듈 import
class QuestionCreateView(CreateView):
    model = Question
    context_object_name = 'question'
    form_class = QuestionForm
    template_name = 'coffee-chat/question/create.html'

    def form_valid(self, form):
        try:
            # 현재 유저의 Alumini 정보 가져오기 시도
            alumini = Alumini.objects.get(user=self.request.user)
            
            temp = form.save(commit=False)
            temp.author = alumini
            temp.save()
            return super().form_valid(form)
            
        except Alumini.DoesNotExist:
            # Alumini 정보가 없으면 에러 페이지나 프로필 생성 페이지로 리다이렉트
            # 여기서는 예시로 메인 페이지로 보내면서 에러 메시지를 남기는 방식입니다.
            # (messages 프레임워크를 쓴다면 user에게 알림을 줄 수 있음)
            # 1. 사용자에게 보낼 메시지 적재 (level: ERROR)
            #messages.error(self.request, "동문 프로필 정보가 없습니다. 프로필을 먼저 생성해주세요!")
            return HttpResponseRedirect(reverse('account:create'))

    def get_success_url(self):
        return reverse('mainpage:qna')


class QuestionDetailView(DetailView):
    model = Question
    context_object_name = 'target_question'
    template_name = 'coffee-chat/question/detail.html'

class QuestionDeleteView(DeleteView):
    model = Question
    context_object_name = 'target_question'
    success_url = reverse_lazy('mainpage:qna')
    template_name = 'coffee-chat/question/delete.html'


############# DRF API #############
from django.http import JsonResponse

def hello(request):
    # GET 요청에서 message 파라미터 읽기
    message = request.GET.get("message", "")
    return JsonResponse({"received_message": message, "status": "success"})
