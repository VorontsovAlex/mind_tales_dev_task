from django.db.models import Manager
from django.apps import apps
from django.db.models import Sum

from restaurant.querysets import VoteQuerySet


class VoteManager(Manager.from_queryset(VoteQuerySet)):
    def get_menus_votes_by_restaurant_and_day_sorted(self, restaurant, day):
        menu_model = apps.get_model('restaurant', 'Menu')

        return self.model.objects.values(
            'menu'
        ).filter(
            menu__in=menu_model.objects.get_menus_by_restaurant_and_day(restaurant, day)
        ).annotate(
            total_score=Sum('score')
        ).order_by(
            '-total_score'
        )
