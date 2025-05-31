from django.urls import path, include
from mainpg.views import MainView
from django.contrib.auth.views import LoginView

app_name = 'mainpage'

urlpatterns = [
    path('main/', LoginView.as_view(template_name='mainpg/intro.html') , name='main'),
]