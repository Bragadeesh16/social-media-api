from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework import generics, mixins
from rest_framework import status
from rest_framework_simplejwt.tokens import (
    RefreshToken,
)
from .models import *
from .serializers import *
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
)


@api_view(["POST"])
def user_register(request):
    if request.method == "POST":
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data["email"] = account.email
            data["response"] = "account has been created"

            refresh = RefreshToken.for_user(account)

            data["token"] = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        else:
            data = serializer.errors

        return Response(data, status=status.HTTP_200_OK)


@api_view(["POST"])
def logout_user(request):
    if request.method == "POST":
        print(request.user.auth_token)
        request.user.auth_token.delete()
        return Response({"message": "your are logged out "})


@api_view(["POST"])
def login_user(request):
    dicti = {}
    if request.method == "POST":
        data = TokenObtainPairSerializer(data=request.data)
        if data.is_valid():
            dicti = {
                "access": data.validated_data["access"],
                "refresh": data.validated_data["refresh"],
            }

    return Response(dicti, status=status.HTTP_200_OK)


class CreateCommunityClass(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CreateCommunitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(
                {"message": "Community is created"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class ListCommunity(generics.GenericAPIView, mixins.ListModelMixin):

    permission_classes = [IsAuthenticated]

    queryset = Community.objects.all()
    serializer_class = CreateCommunitySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class JoinCommunity(generics.GenericAPIView):
    def get(self, request):
        user_in = None
        user_in = Community.objects.filter(member=request.user).exists()
        if user_in:
            return Response({"joined"})
        else:
            return Response({"join"})


@api_view(["POST"])
def SearchCommunity(request):

    permission_classes = [IsAuthenticated]

    if request.method == "POST":
        serializer = SearchCommunitySerializer(data=request.data)
        if serializer.is_valid():
            search_term = serializer.validated_data["search"]
            search_result = Community.objects.filter(
                community_name__contains=search_term
            )
            serialized_data = CreateCommunitySerializer(
                search_result, many=True
            )
            return Response(serialized_data.data)


class DetailViewOfCommunity(generics.GenericAPIView):
    def get(self, request, slug):

        try:
            community = Community.objects.get(slug = slug)
            posts = CommunityPost.objects.filter(community=community)
            community_serializer = CreateCommunitySerializer(community)
            post_serializer = CreatePostSerializer(posts , many = True,context={'request': request})
            response_data = {
                'community': community_serializer.data,
                'posts': post_serializer.data
            }
            return Response(response_data,status=status.HTTP_200_OK)

        except:
            return Response({"community not found"})


class CreatePost(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreatePostSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            community = Community.objects.get(
                community_name=serializer.validated_data["community"]
            )
            community_post = serializer.save(
                author=request.user, community=community
            )
            community_post.counts = community_post.liked_by.count()
            community_post.save()
            return Response(
                {"message": "post is created"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

class Postlike(generics.GenericAPIView):
    pass


class postcommand(generics.GenericAPIView):
    pass
