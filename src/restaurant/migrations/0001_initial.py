# Generated by Django 4.1 on 2023-05-14 06:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'address',
                    models.CharField(
                        max_length=1000, unique=True, verbose_name='Address'
                    ),
                ),
            ],
            options={
                'verbose_name': 'Restaurant',
                'verbose_name_plural': 'Restaurants',
                'db_table': 'restaurant',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('name', models.CharField(max_length=255, verbose_name='Menu name')),
                ('data', models.TextField(verbose_name='Menu content')),
                ('day', models.DateField(verbose_name='Day')),
                (
                    'created_by',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='By whom Menu created',
                    ),
                ),
                (
                    'restaurant',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='restaurant.restaurant',
                        verbose_name='Restaurant',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Menu',
                'verbose_name_plural': 'Menu',
                'db_table': 'menu',
                'unique_together': {('name', 'restaurant', 'day')},
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'score',
                    models.PositiveIntegerField(
                        verbose_name='Count of point given to Menu'
                    ),
                ),
                (
                    'menu',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='votes',
                        to='restaurant.menu',
                        verbose_name='Menu',
                    ),
                ),
                (
                    'voted_by',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='By whom voted',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Vote',
                'verbose_name_plural': 'Votes',
                'db_table': 'vote',
                'unique_together': {('menu', 'voted_by')},
            },
        ),
    ]