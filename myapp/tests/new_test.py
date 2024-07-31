import pytest
from rest_framework.test import APIClient
from myapp.tests.login_test import test_login_user

client = APIClient()


@pytest.mark.django_db
def test_add_community_feature():

    token = test_login_user()

    client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

    payload = {"community_name": "pytest"}

    response = client.post("/create-community/", payload)

    print(response.data)

    assert response.status_code == 201
