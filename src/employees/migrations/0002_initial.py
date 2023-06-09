# Generated by Django 4.1 on 2023-05-14 06:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employees', '0001_initial'),
        ('restaurant', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='restaurant',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to='restaurant.restaurant',
                verbose_name='Restaurant',
            ),
        ),
        migrations.AddField(
            model_name='employee',
            name='user_permissions',
            field=models.ManyToManyField(
                blank=True,
                help_text='Specific permissions for this user.',
                related_name='user_set',
                related_query_name='user',
                to='auth.permission',
                verbose_name='user permissions',
            ),
        ),
    ]
