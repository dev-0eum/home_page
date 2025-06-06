from django.db import models

# Create your models here.
class Account(models.Model):
    name = models.CharField(max_length=50, null=False)
    th = models.IntegerField(default=0)
    company = models.CharField(max_length=100, default='TBA')
    contact = models.CharField(max_length=200, default='TBA')
    introduce = models.TextField()

    img = models.ImageField(upload_to='account/')
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.name