from django.db import models
from accounts.models import Alumini

# Create your models here.
class News(models.Model):
    img = models.ImageField(upload_to='news/')
    title = models.CharField(max_length=50, null=False)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True, null=False)
    
class OrgImg(models.Model):
    img = models.ImageField(upload_to='org/', null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True) # URL 등에 쓰기 좋음

    def __str__(self):
        return self.name

class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='questions')
    author = models.ForeignKey(Alumini, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=100,null=False)
    content = models.TextField(null=False)

    created_at = models.DateTimeField(auto_now_add=True, null=False)

    # question.answers(related_name).all() 
    def __str__(self):
        return f"[{self.category}] {self.title}"

class Answer(models.Model):
    # answer.question.category
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(Alumini, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField(null=False)

    created_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        ordering = ['-created_at'] # 최신 답변 순

    def __str__(self):
        return f"Answer to {self.question.title}"