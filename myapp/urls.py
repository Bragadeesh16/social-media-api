from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('signup',views.user_register,name='signup'),
    path('login',obtain_auth_token, name= 'login'),
    path('logout',views.logout_user, name= 'logout'),
]