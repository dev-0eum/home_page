from django.shortcuts import render
from django.views.generic import *

# Create your views here.
class MainView(DetailView):
    template_name='mainpg/intro.html'