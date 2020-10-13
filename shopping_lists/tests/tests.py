# Create your tests here.
from django.urls import reverse


def test_index(client):
    response = client.get(reverse('index'))
    assert response.status_code == 200