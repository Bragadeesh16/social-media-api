from django.contrib import admin
from .models import *


admin.site.register(CustomUser)
admin.site.register(CommunityPost)
admin.site.register(Community)
admin.site.register(PostCommand)
