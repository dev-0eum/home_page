from django.forms import ModelForm, Select, TextInput, Textarea
from mainpg.models import News, OrgImg, Question, Answer, Category


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

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['title','content','category']

        # 1. 위젯 설정: HTML에서 <select> 태그에 클래스를 부여하여 스타일링
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '제목을 입력하세요'
            }),
            'category': Select(attrs={
                'class': 'form-select'
            }),
            'content': Textarea(attrs={
                'class': 'form-control', 
                'rows': 5, 
                'placeholder': '내용을 입력하세요'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # placeholder ("카테고리를 선택하세요")
        self.fields['category'].empty_label = "카테고리를 선택해주세요"
        

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['content']