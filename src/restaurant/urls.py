from django.urls import path

from restaurant.views import MenuView, RestaurantView, ResultView, VoteView


app_name = 'restaurant'


urlpatterns = [
    path('', RestaurantView.as_view(), name='restaurant'),
    path('menu', MenuView.as_view(), name='menu'),
    path('vote', VoteView.as_view(), name='vote'),
    path('result', ResultView.as_view(), name='results'),
]
