from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'account'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
]