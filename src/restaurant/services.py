from restaurant.models import Menu, Restaurant, Vote


class RestaurantService:
    def get_top_menu_by_restaurant_and_day(self, restaurant: Restaurant, day):
        menus_ranked = Vote.objects.get_menus_votes_by_restaurant_and_day_sorted(restaurant, day)

        if menus_ranked:
            top_menu_with_score = menus_ranked.first()['menu']
            return Menu.objects.get(id=top_menu_with_score)

        return None

    def get_menus_ranked_by_restaurant_and_day(self, restaurant, day):
        return Vote.objects.get_menus_votes_by_restaurant_and_day_ranked(restaurant, day)


class VoteService:
    def get_employee_votes(self, employee, day):
        menus = Menu.objects.get_menus_by_restaurant_and_day(employee.restaurant, day)
        return Vote.objects.filter(menu__in=menus, voted_by=employee)
