import pytest
from django.urls import reverse
from django.contrib.auth.models import Group

from rest_framework.test import APIClient

from employees.models import Employee
from employees.services import EmployeeService
from employees.enums import EmployeeGroup
from restaurant.tests.factories import RestaurantFactory


pytest_plugins = (
    "employees.tests.factories",
    "restaurant.tests.factories",
)

pytestmark = [pytest.mark.django_db]

client = APIClient()


@pytest.fixture
def restaurant():
    return RestaurantFactory(id=111)


@pytest.fixture
def admin_credentials(restaurant):
    return {"login": 'admin_test', 'password': 'Asie6Rx=9', 'restaurant': restaurant}


@pytest.fixture
def admin_employee(admin_credentials):
    service = EmployeeService()
    employee = service.signup(**admin_credentials)
    employee.groups.add(Group.objects.get(name=EmployeeGroup.ADMIN))


# disabled unused-argument warning;
# fixtures are used in tests
# pylint:disable=W0613
@pytest.fixture
def admin_token(admin_credentials, admin_employee: Employee):
    url = reverse("employee:token")
    response = client.post(url, data=admin_credentials)
    token = response.data['token']
    return token


@pytest.fixture
def worker_credentials(restaurant):
    return {"login": 'worker_1', 'password': 'DoQsnc81', 'restaurant': restaurant}


@pytest.fixture
def worker_employee(worker_credentials):
    service = EmployeeService()
    employee = service.signup(**worker_credentials)
    employee.groups.add(Group.objects.get(name=EmployeeGroup.WORKER))
    return employee


@pytest.fixture
def worker_token(worker_credentials, worker_employee: Employee):
    url = reverse("employee:token")
    response = client.post(url, data=worker_credentials)
    token = response.data['token']
    return token
