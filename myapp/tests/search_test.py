import pytest
from rest_framework.test import APIClient
from myapp.tests.login_test import test_login_user
from myapp.models import *

client = APIClient()

@pytest.mark.django_db
def test_search_community_feature():

    token = test_login_user()

    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    Community.objects.create(community_name='django')

    Community.objects.create(community_name='django rest framework')

    Community.objects.create(community_name='django pytest')

    payload = {
        'search':'django'
    }

    response = client.post('/search-community/', payload ,format='json')

    print(response.data)

    assert response.status_code == 200