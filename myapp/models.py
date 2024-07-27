from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import (
    AbstractUser,
)


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(
        blank=True,
        null=True,
        max_length=30,
        unique=True,
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        return super().save(*args, **kwargs)


@receiver(post_save, sender=CustomUser)
def create_username(sender, instance=None, created=False, **kwargs):
    if created:
        email = instance.email
        sliced_email = email.split("@")[0]
        instance.username = sliced_email
        instance.save()


class Community(models.Model):
    """Class is used to creating a community"""

    community_profile = models.ImageField(
        upload_to="community_profile",
        blank=True,
        null=True,
    )
    community_name = models.CharField(max_length=20, unique=True)
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
    )
    members = models.ManyToManyField(
        CustomUser,
        related_name="community_members",
    )


class PostCommand(models.Model):
    """Class is used to create a command"""

    command = models.TextField(blank=True)
    command_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="command_by",
        blank=True,
        null=True,
    )


class CommunityPost(models.Model):
    """Class is used to create a post"""

    title = models.CharField(max_length=200)
    post_image = models.ImageField(
        upload_to="post_image",
        blank=True,
        null=True,
    )
    is_likes = models.BooleanField(default=False)
    count = models.IntegerField(blank=True, default=0)
    description = models.TextField()
    commands = models.ManyToManyField(PostCommand, blank=True)
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        related_name="author",
        null=True,
    )
    liked_by = models.ManyToManyField(
        CustomUser,
        related_name="liked_by",
        blank=True,
    )
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name="community",
        null=True,
    )

    def save(self, *args, **kwargs):
        self.count = len(self.liked_by)
        super().save(*args, **kwargs)
