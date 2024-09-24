from django.shortcuts import render
from django.contrib.auth import authenticate


from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated
from .permissions import UserListPermissions,SellerListPermissions
from .models import SellerProfile,Address
from . import serializers 
from django.contrib.auth import get_user_model



User = get_user_model()


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class UserSignup(APIView):
    def post(self, request):
        serializer = serializers.UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'result':True,'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data['refresh']
        access_token = response.data['access']
        decoded_token = AccessToken(access_token)
        user_id = decoded_token.payload['user_id']
       
        return Response({
            'result':True,
            'user_id':user_id,
            'access': access_token,
            'refresh': refresh_token,
            'message':'login success.'
        })
    

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = serializers.ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            # Get the current user
            user = request.user

            # Check if the provided old password is correct
            old_password = serializer.validated_data.get('old_password')
            if not user.check_password(old_password):
                return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

            # Validate and set the new password
            new_password = serializer.validated_data.get('new_password')

            # Change the password
            user.set_password(new_password)
            user.save()

            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SellerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SellerProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        users= self.request.user
        if users.is_staff:
            return SellerProfile.objects.all()
        user_id=users.id
        return SellerProfile.objects.filter(user=user_id)
    
    def create(self, request):
        # Check if the current user is a seller
        if request.user.is_authenticated and request.user.is_seller:
            mutable_data = request.data.copy()
            # Set the user of the created instance to the request user
            mutable_data['user'] = request.user.id
            serializer = serializers.SellerProfileSerializer(data=mutable_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "only seller user can perform this action."}, status=status.HTTP_403_FORBIDDEN)




    
class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = serializers.AddressSerializer
    
    def get_queryset(self):
        users= self.request.user
        if users.is_staff:
            return Address.objects.all()
        user_id=users.id
        return Address.objects.filter(user=user_id)
    
    def create(self, request):
        # Check if the current user is a authenticated user
        if request.user.is_authenticated :
            mutable_data = request.data.copy()
            # Set the user of the created instance to the request user
            mutable_data['user'] = self.request.user.id 
            serializer = serializers.AddressSerializer(data=mutable_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "only authenticated user can perform this action."}, status=status.HTTP_403_FORBIDDEN)



class UserListViewSet(viewsets.ModelViewSet):
    
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated,UserListPermissions]
    
    def get_queryset(self):
        users= self.request.user
        if users.is_staff:
            return User.objects.all()
        user_id=users.id
        return User.objects.filter(id=user_id)    

