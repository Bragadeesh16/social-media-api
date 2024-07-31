from .models import *
from rest_framework import serializers


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
    )

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "password",
            "password2",
        ]

    def save(self, **kwargs):
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError(
                {"error": "password does not match"}
            )

        if CustomUser.objects.filter(
            email=self.validated_data["email"]
        ).exists():
            raise serializers.ValidationError(
                {"error": "email id is already exists"}
            )

        account = CustomUser(email=self.validated_data["email"])
        account.set_password(password)
        account.save()

        return account


class CreateCommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = [
            "community_profile",
            "community_name",
        ]


class SearchCommunitySerializer(serializers.Serializer):
    search = serializers.CharField(max_length=200)


class CreatePostSerializer(serializers.ModelSerializer):

    community = serializers.ChoiceField(choices=Community.objects.none())

    class Meta:
        model = CommunityPost
        fields = ["title", "post_image", "description", "community"]

    def __init__(self, *args, **kwargs):
        user = kwargs["context"]["request"].user
        super().__init__(*args, **kwargs)
        self.fields["community"].choices = Community.objects.filter(
            members=user
        )
        community_names = tuple(
            [
                tuple((str(i.community_name), i.community_name))
                for i in self.fields["community"].choices
            ]
        )
        self.fields["community"].choices = community_names
