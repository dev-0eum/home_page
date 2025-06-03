from django.shortcuts import render
from django.views.generic import *

from accounts.models import Account

# Create your views here.
class MainView(DetailView):
    template_name='mainpg/intro.html'

class TestView(ListView):
    model = Account
    context_object_name = 'alumini_list'
    template_name = 'feature/test.html'