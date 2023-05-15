from django.contrib.auth.models import UserManager
from django.contrib.auth.hashers import make_password
from django.apps import apps


class CustomUserManager(UserManager):
    def _create_user(self, login, password, **extra_fields):
        if not login:
            raise ValueError('The given login must be set')

        employee_model = apps.get_model('employees', 'Employee')
        user = employee_model(login=login, **extra_fields)
        user.password = make_password(password)
        user.save()
        return user

    def create_user(self, login, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(login, password, **extra_fields)

    def create_superuser(self, login=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(login=login, password=password, **extra_fields)
