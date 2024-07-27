# Generated by Django 5.0.7 on 2024-07-27 17:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0004_remove_communitypost_community_community_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="community",
            name="author",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
