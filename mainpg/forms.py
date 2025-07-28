from django.forms import ModelForm
from mainpg.models import News


class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = ['img','title','content']