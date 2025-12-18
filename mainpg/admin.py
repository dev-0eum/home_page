from django.contrib import admin

from .models import Question, Answer, Category

# Register your models here.
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['pk','title','author','category', 'created_at']
    list_display_links = ['pk', 'title','author','category', 'created_at']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['pk', 'question', 'author', 'created_at']
    list_display_links = ['pk', 'question', 'author', 'created_at']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'slug']
    list_display_links = ['pk', 'name', 'slug']