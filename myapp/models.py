from django.db import models
from django.contrib.auth.models import User

    
class create_community_model(models.Model):
    community_profile = models.ImageField(upload_to='community_profile',blank=True)
    community_name = models.CharField(max_length=20,unique=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    community_type = models.CharField(max_length=7,)
    

class post_command(models.Model):
    command = models.TextField(blank=True)
    command_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='command_by',blank=True,null=True)


class community_post(models.Model):
    title = models.CharField(max_length=200)
    post_image = models.ImageField(upload_to='post_image',blank=True,null=True)
    is_likes = models.BooleanField(default=False)
    count = models.IntegerField(blank=True,default=0)
    description = models.TextField()
    commands = models.ManyToManyField(post_command,blank=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,related_name='author',null=True)
    liked_by = models.ManyToManyField(User,related_name='liked_by',blank=True)
    community = models.ManyToManyField(create_community_model,related_name='posts')

    
    def save(self, *args, **kwargs):
        self.count = len(self.liked_by)
        super().save(*args, **kwargs)