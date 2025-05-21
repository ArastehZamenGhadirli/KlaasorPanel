from rest_framework import serializers
from .models import BlogCategory ,BlogPost
from .models import BlogPost



class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['name']
        
        
        

class BlogPostSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer(read_only=True)
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)

    class Meta:
        model = BlogPost
        fields = [ 'title', 'content', 'category', 'status', 'author_name', 'created_at', 'updated_at']



class BlogPostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'category', 'status']
        
        
        
