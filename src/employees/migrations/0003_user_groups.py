from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.db import migrations, transaction

from employees.enums import EmployeeGroup
from employees.services import EmployeeService


def _create_admin_group():
    return Group.objects.create(name=EmployeeGroup.ADMIN)


def _create_worker_group():
    return Group.objects.create(name=EmployeeGroup.WORKER)


def _create_admin_employee(employee_model, admin_group):
    employee_service = EmployeeService()
    employee = employee_service.signup(
        login='admin',
        password='Ol4iZsa=',
        is_staff=True,
        is_superuser=True
    )
    employee.groups.add(Group.objects.get(name=EmployeeGroup.ADMIN))


def create(apps, schema_editor):
    Employee = apps.get_model('employees', 'Employee')

    with transaction.atomic():
        admin_group = _create_admin_group()
        _create_worker_group()
        _create_admin_employee(Employee, admin_group)


class Migration(migrations.Migration):
    dependencies = [
        ('employees', '0002_initial'),
    ]

    operations = [
        migrations.RunPython(create)
    ]
