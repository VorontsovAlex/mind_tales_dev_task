from django.apps import apps
from django.db.models import F, QuerySet, Sum
from django.db.models.expressions import Window
from django.db.models.functions import RowNumber


class MenuQuerySet(QuerySet):
    def get_menus_by_restaurant_and_day(self, restaurant, day):
        return self.filter(restaurant=restaurant, day=day)


class VoteQuerySet(QuerySet):
    def get_menus_votes_by_restaurant_and_day_ranked(self, restaurant, day):
        menu_model = apps.get_model('restaurant', 'Menu')

        queryset = self.model.objects.values(
            'menu'
        ).filter(
            menu__in=menu_model.objects.get_menus_by_restaurant_and_day(restaurant, day)
        ).annotate(
            total_score=Sum('score'),
            place=Window(expression=RowNumber(), order_by=F('total_score').desc())
        )

        return queryset.values(
            'place', 'menu', 'total_score'
        )
