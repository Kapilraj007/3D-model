from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import GenericAPIView
from . import views



# URLs for the API
urlpatterns = [
    path('create/blog/',views.BlogPostAPIView.as_view(),name='create-blog'),
    path('blogs/',views.BlogListAPIView.as_view(),name='blogs'),
    path('blogs/<int:pk>',views.BlogUpdateDeleteAPIView.as_view(),name='blogs'),
     path('likes/', views.LikeViewSet.as_view()),
    path('likes/<int:pk>/', views.LikeViewSet.as_view()),
    
    
]
