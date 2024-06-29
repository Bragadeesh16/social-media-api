from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(CustomUser, UserAdmin)