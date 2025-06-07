from django.contrib.auth.models import User
from django.http import HttpResponseForbidden

def account_ownership_required(func):
    def decorated(request, *args,**kwargs):
        user = User.objects.get(pk=kwargs['pk'])
        if not user == request.user:
            return HttpResponseForbidden()
        return func(request,*args,**kwargs)
    return decorated


from .models import Alumini
from django.http import HttpResponseForbidden

def profile_ownership_required(func):
    def decorated(request, *args,**kwargs):
        alumini = Alumini.objects.get(pk=kwargs['pk'])
        if not alumini.user == request.user:
            return HttpResponseForbidden()
        return func(request,*args,**kwargs)
    return decorated