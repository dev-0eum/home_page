from django.db import models

# Create your models here.
class News(models.Model):
    img = models.ImageField(upload_to='news/')
    title = models.CharField(max_length=50, null=False)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True, null=False)
    
class OrgImg(models.Model):
    img = models.ImageField(upload_to='org/', null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)