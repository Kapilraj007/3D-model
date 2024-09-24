from rest_framework import serializers
from .models import Post,Like

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ['created_at','likes']
        
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('post', 'user')