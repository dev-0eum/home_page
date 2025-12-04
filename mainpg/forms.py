from django.forms import ModelForm
from mainpg.models import News, OrgImg


class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = ['img','title','content']


class NewsUpdateForm(NewsForm):
    def __init__(self,*args,**kwargs):
        # TypeError: descriptor '__init__' of 'super' object needs an argument
        # super >> super()로 변경
        super().__init__(*args,**kwargs)
        
class OrgForm(ModelForm):
    class Meta:
        model = OrgImg
        fields = ['img']