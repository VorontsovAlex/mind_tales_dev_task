import datetime
from collections import OrderedDict
from unittest.mock import patch

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.exceptions import ErrorDetail
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED
from rest_framework.test import APIClient

from employees.tests.factories import EmployeeFactory
from restaurant.constants import API_VERSION_NOT_SPECIFIED_MSG
from restaurant.tests.factories import MenuFactory, VoteFactory

pytestmark = [pytest.mark.django_db]

client = APIClient()


@pytest.mark.parametrize(
    'address', [('street_1', ), ('street_2', )]
)
def test_restaurant_create_success(admin_token, address):
    url = reverse('restaurant:restaurant')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')
    response = client.post(url, data={'address': address})
    assert response.status_code == HTTP_201_CREATED


@pytest.mark.parametrize(
    'address, exception_type', [(None, TypeError)]
)
def test_restaurant_create_empty_address(admin_token, address, exception_type):
    url = reverse('restaurant:restaurant')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')
    with pytest.raises(exception_type):
        client.post(url, data={'address': address})


@pytest.mark.parametrize(
    'address_1, address_2',
    [
        ('street_1', 'street_1'),
    ]
)
def test_restaurant_create_duplicates(admin_token, address_1, address_2):
    url = reverse('restaurant:restaurant')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

    response = client.post(url, data={'address': address_1})
    assert response.status_code == HTTP_201_CREATED

    response = client.post(url, data={'address': address_2})

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.data == {
        'address': [ErrorDetail(string='Restaurant with this Address already exists.', code='unique')]
    }


@pytest.mark.parametrize(
    'name, data',
    [
        ('menu_1', 'item1 - price_1; item2 - price2'),
    ]
)
def test_create_menu_success(worker_token, name, data):
    url = reverse('restaurant:menu')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {worker_token}')
    response = client.post(url, data={'name': name, 'data': data}, format='json')
    assert response.status_code == HTTP_201_CREATED


@pytest.mark.parametrize(
    'name, data, response_message',
    [
        (
            'menu_1',
            None,
            {'data': [ErrorDetail(string='This field may not be null.', code='null')]}
        ),
        (
            None,
            'item1 - price_1; item2 - price2',
            {'name': [ErrorDetail(string='This field may not be null.', code='null')]}
        ),
        (
            None,
            None,
            {
                'name': [ErrorDetail(string='This field may not be null.', code='null')],
                'data': [ErrorDetail(string='This field may not be null.', code='null')]
            }
        ),
    ]
)
def test_create_menu_without_required_arguments(worker_token, name, data, response_message):
    url = reverse('restaurant:menu')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {worker_token}')
    response = client.post(url, data={'name': name, 'data': data}, format='json')
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.data == response_message


def test_menu_get_no_votes_given(worker_token, worker_employee):
    MenuFactory(name='name_1', created_by=worker_employee)
    url = reverse('restaurant:menu')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {worker_token}')
    response = client.get(url)
    assert response.status_code == HTTP_404_NOT_FOUND


def test_menu_get_one_vote_several_menus(worker_token, restaurant):
    with patch('django.utils.timezone.now', return_value=datetime.datetime(year=2023, month=5, day=14)):
        fixed_dt = timezone.now().date()

        employee_1 = EmployeeFactory(login='employee_1', password='password_1', restaurant=restaurant)

        menu_1 = MenuFactory(
            name='menu_1', data='data_1', created_by=employee_1, day=fixed_dt, restaurant=restaurant
        )
        _ = MenuFactory(name='menu_2', data='data_2', created_by=employee_1, day=fixed_dt, restaurant=restaurant)

        VoteFactory(menu=menu_1, voted_by=employee_1, score=3)

        url = reverse('restaurant:menu')
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {worker_token}')
        response = client.get(url)
        assert response.status_code == HTTP_200_OK
        assert response.data == {
            'name': 'menu_1', 'data': 'data_1', 'restaurant': 111, 'day': '2023-05-14', 'created_by': 15
        }


def test_menu_get_several_votes(worker_token, restaurant):
    fixed_dt = datetime.datetime(year=2023, month=5, day=14)

    with patch('django.utils.timezone.now', return_value=fixed_dt):
        employee_1 = EmployeeFactory(login='employee_1', password='password_1', restaurant=restaurant)
        employee_2 = EmployeeFactory(login='employee_2', password='password_2', restaurant=restaurant)

        menu_1 = MenuFactory(name='menu_1', data='data_1', created_by=employee_1, day=fixed_dt, restaurant=restaurant)
        menu_2 = MenuFactory(name='menu_2', data='data_2', created_by=employee_1, day=fixed_dt, restaurant=restaurant)
        menu_3 = MenuFactory(name='menu_3', data='data_3', created_by=employee_2, day=fixed_dt, restaurant=restaurant)

        VoteFactory(menu=menu_1, voted_by=employee_1, score=1)
        VoteFactory(menu=menu_2, voted_by=employee_1, score=3)
        VoteFactory(menu=menu_3, voted_by=employee_1, score=2)

        VoteFactory(menu=menu_1, voted_by=employee_2, score=2)
        VoteFactory(menu=menu_2, voted_by=employee_2, score=1)
        VoteFactory(menu=menu_3, voted_by=employee_2, score=3)

        url = reverse('restaurant:menu')
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {worker_token}')
        response = client.get(url)
        assert response.status_code == HTTP_200_OK
        assert response.data == {
            'name': 'menu_3', 'data': 'data_3', 'restaurant': 111, 'day': '2023-05-14', 'created_by': 18
        }


def test_vote_api_v1(worker_token, worker_employee, restaurant):
    url = reverse('restaurant:vote')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {worker_token}', HTTP_BUILD_VERSION='1.0')
    fixed_dt = datetime.datetime(year=2023, month=5, day=14)
    menu_1 = MenuFactory(name='menu_1', data='data_1', created_by=worker_employee, day=fixed_dt, restaurant=restaurant)

    response = client.post(url, data={'menu': menu_1.pk}, format='json')
    assert response.status_code == HTTP_201_CREATED


def test_vote_api_v2(worker_token, worker_employee, restaurant):
    url = reverse('restaurant:vote')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {worker_token}', HTTP_BUILD_VERSION='2.0')
    fixed_dt = datetime.datetime(year=2023, month=5, day=14)
    menu_1 = MenuFactory(name='menu_1', data='data_1', created_by=worker_employee, day=fixed_dt, restaurant=restaurant)
    menu_2 = MenuFactory(name='menu_2', data='data_2', created_by=worker_employee, day=fixed_dt, restaurant=restaurant)
    menu_3 = MenuFactory(name='menu_3', data='data_3', created_by=worker_employee, day=fixed_dt, restaurant=restaurant)

    response = client.post(
        url,
        data=[
            {
                'menu': menu_3.pk,
                'place': 1
            },
            {
                'menu': menu_1.pk,
                'place': 2
            },
            {
                'menu': menu_2.pk,
                'place': 3
            }
        ],
        format='json'
    )
    assert response.status_code == HTTP_201_CREATED


def test_vote_api_no_version(worker_token, worker_employee, restaurant):
    url = reverse('restaurant:vote')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {worker_token}')
    fixed_dt = datetime.datetime(year=2023, month=5, day=14)
    menu_1 = MenuFactory(name='menu_1', data='data_1', created_by=worker_employee, day=fixed_dt, restaurant=restaurant)

    response = client.post(url, data={'menu': menu_1.pk}, format='json')
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.data == {'message': API_VERSION_NOT_SPECIFIED_MSG}


def test_result_success(worker_token, restaurant):
    fixed_dt = datetime.datetime(year=2023, month=5, day=14)

    with patch('django.utils.timezone.now', return_value=fixed_dt):
        employee_1 = EmployeeFactory(login='employee_1', password='password_1', restaurant=restaurant)
        employee_2 = EmployeeFactory(login='employee_2', password='password_2', restaurant=restaurant)
        employee_3 = EmployeeFactory(login='employee_3', password='password_3', restaurant=restaurant)

        menu_1 = MenuFactory(name='menu_1', data='data_1', created_by=employee_1, day=fixed_dt, restaurant=restaurant)
        menu_2 = MenuFactory(name='menu_2', data='data_2', created_by=employee_2, day=fixed_dt, restaurant=restaurant)
        menu_3 = MenuFactory(name='menu_3', data='data_3', created_by=employee_3, day=fixed_dt, restaurant=restaurant)

        VoteFactory(menu=menu_1, voted_by=employee_1, score=3)
        VoteFactory(menu=menu_2, voted_by=employee_1, score=1)
        VoteFactory(menu=menu_3, voted_by=employee_1, score=2)

        VoteFactory(menu=menu_1, voted_by=employee_2, score=1)
        VoteFactory(menu=menu_2, voted_by=employee_2, score=2)
        VoteFactory(menu=menu_3, voted_by=employee_2, score=3)

        VoteFactory(menu=menu_1, voted_by=employee_3, score=3)

        url = reverse('restaurant:results')
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {worker_token}')
        response = client.get(url)
        assert response.status_code == HTTP_200_OK
        assert response.data == [
            OrderedDict([('place', 1), ('menu', 13), ('total_score', 7)]),
            OrderedDict([('place', 2), ('menu', 15), ('total_score', 5)]),
            OrderedDict([('place', 3), ('menu', 14), ('total_score', 3)])
        ]

def test_result_empty(worker_token):
    url = reverse('restaurant:results')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {worker_token}')
    response = client.get(url)
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.data == {
        'message': 'Results not available; Either no menu uploaded yet or no votes are given to any menus'
    }
