from django.urls import path, include
from mainpg.views import *
from django.views.generic import *

app_name = 'mainpage'

urlpatterns = [
    path('home/', home_view , name='home'),
    path('test/', TestView.as_view(), name='test'),
    path("api/text/", hello),
]