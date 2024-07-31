import pytest
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
def test_register_user():
    payload = {
        "email": "test@gmail.com",
        "password": "nagarani",
        "password2": "nagarani",
    }
    response = client.post("/register/", payload)
    data = response.data
