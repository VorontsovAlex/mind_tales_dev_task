from django.db import models

from restaurant.managers import VoteManager
from restaurant.querysets import MenuQuerySet


class Restaurant(models.Model):
    address = models.CharField(max_length=1000, unique=True, verbose_name='Address')

    class Meta:
        db_table = 'restaurant'
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'

    def __str__(self):
        return self.address


class Menu(models.Model):
    name = models.CharField(max_length=255, verbose_name='Menu name')
    data = models.TextField(verbose_name='Menu content')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name='Restaurant')
    day = models.DateField(verbose_name='Day')
    created_by = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, verbose_name='By whom Menu created')

    objects = MenuQuerySet.as_manager()

    class Meta:
        db_table = 'menu'
        verbose_name = 'Menu'
        verbose_name_plural = 'Menu'
        unique_together = ('name', 'restaurant', 'day')


class Vote(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='votes', verbose_name='Menu')
    score = models.PositiveIntegerField(verbose_name='Count of point given to Menu')
    voted_by = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, verbose_name='By whom voted')

    objects = VoteManager()

    class Meta:
        db_table = 'vote'
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'
        unique_together = ('menu', 'voted_by')
