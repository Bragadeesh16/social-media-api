from .models import *
from rest_framework import serializers


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only = True,style = {'input_type':'password'})
    class Meta:
        model = CustomUser
        fields = ['email','password','password2']

    def save(self, **kwargs):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'error':'password does not match'})
        
        if CustomUser.objects.filter(email = self.validated_data['email']).exists():
            raise serializers.ValidationError({'error':'email id is already exists'})
        
        account  = CustomUser(email = self.validated_data['email'])
        account.set_password(password)
        account.save()

        return account
    
class CreateCommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateCommunity
        fields = ['community_profile','community_name',]