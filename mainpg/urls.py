from django.urls import path, include
from mainpg.views import MainView, TestView
from django.contrib.auth.views import LoginView

app_name = 'mainpage'

urlpatterns = [
    path('home/', LoginView.as_view(template_name='mainpg/intro.html') , name='home'),
    path('test/', TestView.as_view(), name='test'),
]