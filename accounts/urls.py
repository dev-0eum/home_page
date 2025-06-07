from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from accounts.views import *

app_name = 'account'

urlpatterns = [
    # For LogIn&Out
    path('login/', LoginView.as_view(template_name='accounts/login.html',next_page='mainpage:home'), name='login'),
    path('logout/', PostLogoutView.as_view(), name='logout'),
    # For User
    path('signup/', UserCreateView.as_view(), name='signup'),
    path('detail/<int:pk>', AccountDetailView.as_view(), name='detail'),
    path('update/<int:pk>', AccountUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', AccountDeleteView.as_view(), name='delete'),
    # For Alumini Profile
    path('create/', AluminiCreateView.as_view(), name='create'),
]