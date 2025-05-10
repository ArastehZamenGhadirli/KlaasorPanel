from rest_framework.serializers  import ModelSerializer
from accounts.models import Team  , CustomUser 
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from rest_framework import permissions


class AccountsSerializer(ModelSerializer):
    class Meta :
        model = CustomUser ,
        feilds = '__all__',
        read_only_fields = ['phone_number']
        write_only_fields= ['first_name','last_name','gender','birth_date','address','email','national_id']
        
    
    #def validate(self, attrs):
    #    """
    #    this function is for validating the password 
    #    it is used in signin view 
    #    """
    #    validated_data = super().validate(attrs)
    #    validated_data['password']  = make_password(validated_data['password'])
    #    return validated_data
    
    
    
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
    
