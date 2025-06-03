from django.shortcuts import render
from django.urls import reverse
from django.views.generic import *

from accounts.forms import AluminiForm
from accounts.models import Account

# Create your views here.
class CreateAccount(CreateView):
    model = Account
    context_object_name = 'target_alumini'
    form_class = AluminiForm
    template_name = 'accounts/create.html'

    # Form을 임시로 받아서, temp의 정보와 req의 정보가 동일한지 체크
    def form_valid(self, form):
        # temp에 form 임시 저장 
        temp = form.save(commit=False)

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