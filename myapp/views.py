from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics,mixins
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from .models import *
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

@api_view(['POST'])
def user_register(request):
    if request.method == 'POST':
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['email'] = account.email
            data['response'] = 'account has been created'

            refresh = RefreshToken.for_user(account)

            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        else:
            data = serializer.errors

        return Response(data)  
    

@api_view(['POST'])
def logout_user(request):
    if request.method == 'POST':
        print(request.user.auth_token)
        request.user.auth_token.delete()
        return Response({'message':'your are logged out '})
    
@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        data = TokenObtainPairSerializer(data=request.data)
        print('hello')
        if data.is_valid():
            dicti = {
                'access':data.validated_data['access'],
                'refresh':data.validated_data['refresh']
            }

    return Response(dicti)

class CreateCommunityClass(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]

    def post(self,request,*args,**kwargs):
        serializer = CreateCommunitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author = request.user)
            return Response({'message': 'Community is created'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ListCommunity(generics.GenericAPIView):
    pass

class JoinCommunity(generics.GenericAPIView):
    pass

class SearchCommunity(generics.GenericAPIView):
    pass

class CreatePost(generics.GenericAPIView):
    pass

class DetailViewOfCommunity(generics.GenericAPIView):
    pass