from django.forms import ModelForm
from accounts.models import Alumini


class AluminiForm(ModelForm):
    class Meta:
        model = Alumini
        fields = ['img','name','th','company','contact','introduce']


from django.contrib.auth.forms import UserCreationForm
class AccountUpdateForm(UserCreationForm):
    def __init__(self,*args,**kwargs):
        # TypeError: descriptor '__init__' of 'super' object needs an argument
        # super >> super()로 변경
        super().__init__(*args,**kwargs)
        
        self.fields['name'].disabled = True