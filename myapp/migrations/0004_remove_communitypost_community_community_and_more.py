# Generated by Django 5.0.7 on 2024-07-26 11:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0003_remove_createcommunity_community_type_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="communitypost",
            name="community",
        ),
        migrations.CreateModel(
            name="Community",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "community_profile",
                    models.ImageField(
                        blank=True, null=True, upload_to="community_profile"
                    ),
                ),
                ("community_name", models.CharField(max_length=20, unique=True)),
                (
                    "author",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "members",
                    models.ManyToManyField(
                        related_name="community_members", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="CreateCommunity",
        ),
        migrations.AddField(
            model_name="communitypost",
            name="community",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="community",
                to="myapp.community",
            ),
        ),
    ]
