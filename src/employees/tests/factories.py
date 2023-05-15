import factory
from pytest_factoryboy import register


@register
class EmployeeFactory(factory.django.DjangoModelFactory):
    login = factory.Sequence(lambda n: f'login {n}')
    password = factory.Sequence(lambda n: f'password {n}')
    restaurant = factory.SubFactory('restaurant.tests.factories.RestaurantFactory')

    class Meta:
        model = 'employees.Employee'
