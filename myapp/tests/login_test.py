import pytest
from rest_framework.test import APIClient
from myapp.models import CustomUser
from django.urls import reverse

client = APIClient()

@pytest.mark.django_db
def test_login_user():

    user = CustomUser.objects.create(email='test@gmail.com')
    user.set_password('bragadeesh')
    user.save()

    payload = {
        'email': 'test@gmail.com',
        'password': 'bragadeesh'
    }

    response = client.post(reverse('login'), payload, format='json')

    data = response.data
    assert response.status_code == 200
    return data['access']
