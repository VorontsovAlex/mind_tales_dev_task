from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from employees.managers import CustomUserManager


class Employee(AbstractBaseUser, PermissionsMixin):
    '''
    Represent Restaurant Employees
    '''
    login = models.CharField(max_length=255, unique=True, verbose_name='Login')
    is_staff = models.BooleanField(default=False, verbose_name='Access to admin site')
    is_active = models.BooleanField(default=True, verbose_name='Active Account')
    restaurant = models.ForeignKey(
        'restaurant.Restaurant', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Restaurant'
    )

    objects = CustomUserManager()
    USERNAME_FIELD = 'login'

    class Meta:
        db_table = 'employee'
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
