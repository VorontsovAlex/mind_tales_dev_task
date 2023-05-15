import factory
from pytest_factoryboy import register
from factory import Faker
from django.utils.timezone import get_current_timezone


@register
class RestaurantFactory(factory.django.DjangoModelFactory):
    address = factory.Sequence(lambda n: f'address {n}')

    class Meta:
        model = 'restaurant.Restaurant'


@register
class MenuFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'Menu_{n+1}')
    data = factory.Sequence(lambda n: f'Item_{n+1} Item_{n+2} Item_{n+3}')
    restaurant = factory.SubFactory(RestaurantFactory)
    day = Faker('date_time_this_year', tzinfo=get_current_timezone())
    created_by = factory.SubFactory('employees.tests.factories.EmployeeFactory')

    class Meta:
        model = 'restaurant.Menu'


@register
class VoteFactory(factory.django.DjangoModelFactory):
    menu = factory.SubFactory(MenuFactory)
    score = 0
    voted_by = factory.SubFactory('employees.tests.factories.EmployeeFactory')

    class Meta:
        model = 'restaurant.Vote'
