from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from restaurant.models import Restaurant, Menu, Vote
from restaurant.constants import ELEGIBLE_VOTING_PLACES, SCORE_MAPPER


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['address']


class RestaurantResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'address']


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['name', 'data', 'restaurant', 'day', 'created_by']


class MenuResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'name', 'data', 'restaurant', 'day', 'created_by']


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['menu', 'score', 'voted_by']


class VotesTop3Serializer(serializers.Serializer):
    unique_menus = None
    unique_places = None
    place = serializers.IntegerField()
    menu = serializers.PrimaryKeyRelatedField(queryset=Menu.objects.all())
    score = serializers.SerializerMethodField('get_score')
    voted_by = serializers.SerializerMethodField('get_voted_by')

    def get_voted_by(self, _):
        return self.context['request'].user.pk

    def get_score(self, instance):
        return SCORE_MAPPER[instance['place']]

    def validate(self, attrs):
        if not self.unique_menus:
            self.unique_menus = set()

        if attrs['place'] in self.unique_menus:
            raise ValidationError('Menu values are not unique')
        self.unique_menus.add(attrs['menu'])

        if not self.unique_places:
            self.unique_places = set()

        if attrs['place'] in self.unique_places:
            raise ValidationError('Places values are not unique')
        self.unique_places.add(attrs['place'])

        if attrs['place'] not in ELEGIBLE_VOTING_PLACES:
            raise ValidationError('Invalid place value. Must be range from 1 to 3')

        return attrs


class ResultSerializer(serializers.Serializer):
    place = serializers.IntegerField()
    menu = serializers.IntegerField()
    total_score = serializers.IntegerField()
