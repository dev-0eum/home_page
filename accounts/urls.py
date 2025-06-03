from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from accounts.views import CreateAccount

app_name = 'account'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('create/', CreateAccount.as_view(), name='create'),
]