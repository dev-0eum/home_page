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