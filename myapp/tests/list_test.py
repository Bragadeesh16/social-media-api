import pytest
from rest_framework.test import APIClient
from myapp.tests.login_test import test_login_user
from myapp.models import *

client = APIClient()


@pytest.mark.django_db
def test_list_community_feature():

    token = test_login_user()

    client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

    Community.objects.create(community_name="Community 1")

    response = client.get("/community-list/")

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["community_name"] == "Community 1"
