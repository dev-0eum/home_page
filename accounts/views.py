from django.shortcuts import render
from django.urls import reverse
from django.views.generic import *

# For Alumini
from accounts.forms import AluminiForm
from accounts.models import Alumini

# For User
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from accounts.forms import AccountUpdateForm
from django.http import *

# decorators
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from accounts.decorators import account_ownership_required, profile_ownership_required
has_ownership=[account_ownership_required, login_required]

# Create your views here.
# Alumini(Profile)
class AluminiCreateView(CreateView):
    model = Alumini
    context_object_name = 'target_alumini'
    form_class = AluminiForm
    template_name = 'alumini/create.html'

    # Form을 임시로 받아서, temp의 정보와 req의 정보가 동일한지 체크
    def form_valid(self, form):
        # temp에 form 임시 저장 
        temp = form.save(commit=False)
        
        # alumini에 user 정보를 연결
        temp.user = self.request.user
        # models.py에서 객체의 user가 request의 user와 동일한지 체크
        #temp.user = self.request.user


        # 실제로 데이터 저장
        temp.save()

        return super().form_valid(form)
    
    # Redirect to URL
    def get_success_url(self):
        return reverse('mainpage:home')
        # Redirect with PK param
        # return reverse('account:detail',kwargs={'pk': self.object.user.pk})

@method_decorator(profile_ownership_required, 'get')
@method_decorator(profile_ownership_required, 'post')
class ProfileUpdateView(UpdateView):
    model = Alumini
    context_object_name = 'target_profile'
    form_class = AluminiForm
    #success_url = reverse_lazy('account:greeting')
    template_name = 'alumini/update.html'

    def get_success_url(self):
        return reverse('account:detail',kwargs={'pk': self.object.user.pk})


# User
class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('mainpage:home') # class에서는 lazy 사용
    template_name = 'accounts/create.html'

class AccountDetailView(DetailView):
    model = User
    context_object_name = 'target_user'
    template_name = 'accounts/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Check 'Search' Permission
        user = self.request.user
        context['can_view'] = user.groups.filter(name='search').exists()
        # End
        # Check user has profile
        try:
            context['alumini_profile'] = self.get_object().profile
        except Alumini.DoesNotExist:
            context['alumini_profile'] = None
        return context

class AccountUpdateView(UpdateView):
    model = User
    form_class = AccountUpdateForm # id가 변경 가능한 폼 >> 그래서 새로운 폼
    context_object_name = 'target_user'
    success_url = reverse_lazy('mainpage:home')
    template_name = 'accounts/update.html'

    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated and self.get_object() == self.request.user:
            return super().get(*args,**kwargs)
        else:
            return HttpResponseForbidden()
        
    def post(self,*args,**kwargs):
        if self.request.user.is_authenticated and self.get_object() == self.request.user:
            return super().post(*args,**kwargs)
        else:
            return HttpResponseForbidden()

@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountDeleteView(DeleteView):
    model = User
    context_object_name = 'target_user'
    success_url = reverse_lazy('mainpage:home')
    template_name = 'accounts/delete.html'


from django.contrib.auth.views import LogoutView
class PostLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)