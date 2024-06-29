from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from rest_framework import generics,mixins
from rest_framework import status
from rest_framework.authtoken.models import Token

@api_view(['POST'])
def user_register(request):
    if request.method == 'POST':
        serializer = user_register_serializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['email'] = account.email
            data['response'] = 'account has been created'

            token = Token.objects.get(user = account).key
            data['token'] = token

        else:
            data = serializer.errors

        return Response(data)

@api_view(['POST'])
def logout_user(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response({'your are successfully logged out'})

    

