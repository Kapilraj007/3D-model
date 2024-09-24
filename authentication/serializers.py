
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import SellerProfile ,Address




User = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email','phone_number', 'password']
        
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['phone_number'] = instance.phone_number
    #     return representation

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, data):
        # Check if new_password and confirm_new_password match
        new_password = data.get('new_password')
        confirm_new_password = data.get('confirm_new_password')
        if new_password != confirm_new_password:
            raise serializers.ValidationError("New passwords do not match")

        return data
 
 
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model= Address
        fields = ['id','user','house_number_street_area','locality_town','city','state','pincode']
        #read_only_fields = ['user']
       
 
class SellerProfileSerializer(serializers.ModelSerializer):
    # Add fields from the related CustomUser model
    user_firstname = serializers.CharField(source='user.first_name',read_only=True)
    user_lastname = serializers.CharField(source='user.last_name',read_only=True)
    username=serializers.CharField(source='user.username', read_only=True)
    user_address = serializers.SerializerMethodField()

    class Meta:
        model = SellerProfile
        fields = ['id','user','username', 'user_firstname', 'user_lastname', 'brand_name', 'user_address', 'profile_image', 'permit_image', 'license_image']
        #read_only_fields = ['user']

    def get_user_address(self, obj):
        uid = obj.user.id
        address = Address.objects.filter(user_id=uid)
        if address:
            address_serializer = AddressSerializer(address,many=True)
            return address_serializer.data
        return None
    

    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email','phone_number','first_name','last_name','is_seller']  # Add more fields as needed
