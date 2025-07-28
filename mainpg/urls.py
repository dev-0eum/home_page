from django.urls import path, include
from mainpg.views import *
from django.views.generic import *

app_name = 'mainpage'

urlpatterns = [
    path('home/', home_view , name='home'),
    path('test/', TestView.as_view(), name='test'),
    path('search/', SearchView.as_view() ,name='search'),
    path('news/', NewsView.as_view(), name='news'),
    path('upload_news/', NewsCreateView.as_view(), name='upload'),
    path("api/text/", hello),
]