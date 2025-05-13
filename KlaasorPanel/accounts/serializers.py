from rest_framework.serializers  import ModelSerializer
from accounts.models import Team  , CustomUser 
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from rest_framework import permissions
from rest_framework import serializers

class AccountsSerializer(ModelSerializer):
    class Meta :
        model = CustomUser ,
        fields = ['phone_number','first_name','last_name','gender','birth_date','address','email','national_id']
        
        

    
    
class SignUpSerializer(ModelSerializer):
    """
    Its for registeration 
    """
    class Meta :
        model = CustomUser
        fields = ['phone_number']
        extra_kwargs = {
            
            'phone_number': {'required': True}
        }
    
    def create(self, validated_data):
        """
        hash password and create user 
        """
        return super().create(validated_data)



class SignInSerializer(ModelSerializer):
    """
    this login is without otp 
    """
    
    class Meta:
        model : CustomUser 
        fields  = ['phone_number' , 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'phone_number': {'required': True}
        }
    
    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')
        
        user = authenticate(
        request = self.context.get('request'),
        phone_number = phone_number,
        password = password 
        
         
        )
        if not user :
            raise ValidationError(
                {
                    'non_field_errors': ['User account is disabled']
                }   
            )
        
        attrs['user'] = user
        return attrs
    
    def create(self, validated_data):
        #  for  ModelSerializer
        return CustomUser.objects.create_user(**validated_data)
    



class SendOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)

    def validate_phone_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        return value


class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)

    def validate_otp(self, value):
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("OTP must be a 6-digit number.")
        return value