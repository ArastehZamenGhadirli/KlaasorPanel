from django.db import models
from accounts.models import CustomUser 
# Create your models here.


class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class BlogPost(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'پیش‌نویس'
        PUBLISHED = 'PUBLISHED', 'منتشر شده'

    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name='posts')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title    
    





