from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

router=DefaultRouter()
router.register('seller', views.SellerProfileViewSet,basename='seller')
router.register('address', views.AddressViewSet)
router.register('profile', views.UserListViewSet, basename='users')


urlpatterns = [
    path('signup/', views.UserSignup.as_view(), name='signup'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('changepsword/', views.ChangePasswordView.as_view(), name='change_password'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls 

