from django.forms import ModelForm
from accounts.models import Account


class AluminiForm(ModelForm):
    class Meta:
        model = Account
        fields = ['img','name','th','company','contact','introduce']