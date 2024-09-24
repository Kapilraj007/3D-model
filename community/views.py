from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import RetrieveModelMixin,CreateModelMixin,ListModelMixin,UpdateModelMixin,DestroyModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework import generics
from .models import Post,Like
from .serializers import BlogSerializer,BlogPostSerializer,LikeSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
# Create your views here.

class BlogPostAPIView(
                          CreateModelMixin,
                          GenericAPIView):
    queryset = Post.objects.all()
    
    serializer_class = BlogPostSerializer
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class BlogListAPIView(ListModelMixin,GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = BlogSerializer
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
   


class BlogUpdateDeleteAPIView(RetrieveModelMixin,
                              UpdateModelMixin,
                              DestroyModelMixin,
                              GenericAPIView):

    queryset = Post.objects.all()
    serializer_class = BlogPostSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class LikeViewSet(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    
    def post(self, request, *args, **kwargs):
        post_id = request.data.get('post')
        post = get_object_or_404(Post, id=post_id)
        user_id = request.user.id
        like, created = Like.objects.get_or_create(user_id=user_id, post=post)
        if not created:
            return Response({"message": "You already liked this post."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Post liked successfully."}, status=status.HTTP_201_CREATED)