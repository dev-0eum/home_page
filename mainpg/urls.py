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
    path('detail/<int:pk>', NewsDetailView.as_view(), name='detail'),
    path('update/<int:pk>', NewsUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', NewsDeleteView.as_view(), name='delete'),
    # org
    path('org/', OrgView.as_view(), name='org'),
    path('org_add/', OrgCreateView.as_view(), name='org_add'),
    path('org_del/', OrgDeleteView.as_view(), name='org_del'),
    # question
    path('qna/', QNAView.as_view(), name='qna'),
    path('feed/<int:category_id>/', FeedView.as_view(), name='feed'),
    path('atti_detail/', AttiDetailView.as_view(), name='atti_detail'),
    path('exp_feed/', ExpView.as_view(), name='experience'),
    path('ask/', QuestionCreateView.as_view(), name='ask'),
    path('question/<int:pk>', QuestionDetailView.as_view(), name='question_detail'),
    path('question/<int:pk>/delete/', QuestionDeleteView.as_view(), name='question_delete'),
    #path('question/<int:pk>/answer/', AnswerCreateView.as_view(), name='answer_create'),

    # api
    path("api/text/", hello),
]