from django.shortcuts import render
from django.views.generic import *

from accounts.models import Alumini

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
        print(user.groups.all)
        context['is_admin'] = user.groups.filter(name='admin').exists()
        return context




from django.http import JsonResponse

def hello(request):
    # GET 요청에서 message 파라미터 읽기
    message = request.GET.get("message", "")
    return JsonResponse({"received_message": message, "status": "success"})
