import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED

pytestmark = [pytest.mark.django_db]

client = APIClient()


def test_create_worker_employee_by_admin_employee(admin_token, restaurant):
    url = reverse('employee:signup')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')
    response = client.post(
        url,
        data={'login': 'new_worker_1', 'password': 'password_1', 'role': 'Worker', 'restaurant': restaurant.pk},
        format='json'
    )
    assert response.status_code == HTTP_201_CREATED


def test_create_employee_by_worker_employee(worker_token, restaurant):
    url = reverse('employee:signup')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {worker_token}')
    response = client.post(
        url,
        data={'login': 'new_worker_1', 'password': 'password_1', 'role': 'Worker', 'restaurant': restaurant.pk},
        format='json'
    )
    assert response.status_code == HTTP_403_FORBIDDEN


def test_create_employee_without_authoraztion():
    url = reverse('employee:signup')
    response = client.post(url, data={'login': 'new_worker_1', 'password': 'password_1'}, format='json')
    assert response.status_code == HTTP_401_UNAUTHORIZED
