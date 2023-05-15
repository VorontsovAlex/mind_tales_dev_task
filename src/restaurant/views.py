from django.conf import settings
from django.db import transaction
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from app.permissions import IsAdmin, IsWorker
from app.versioning import BuildVersionScheme
from restaurant.constants import API_VERSION_NOT_SPECIFIED_MSG, RESULTS_NOT_AVAILABLE_MSG, SCORE_MAPPER
from restaurant.schemes import (
    menu_get_response_body_schema, menu_post_response_body_schema, restaurant_response_body_schema,
    results_response_body_schema, vote_response_body_schema
)
from restaurant.serializers import (
    MenuResponseSerializer, MenuSerializer, RestaurantResponseSerializer, RestaurantSerializer, ResultSerializer,
    VoteSerializer, VotesTop3Serializer
)
from restaurant.services import RestaurantService, VoteService


class RestaurantView(APIView):
    permission_classes = (IsAuthenticated, IsAdmin)

    @swagger_auto_schema(
        request_body=RestaurantSerializer,
        operation_summary='Creates a restaurant with specified address',
        responses=restaurant_response_body_schema
    )
    def post(self, request):
        serializer = RestaurantSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        restaurant = serializer.save()
        response_serializer = RestaurantResponseSerializer(restaurant)
        return Response(status=HTTP_201_CREATED, data=response_serializer.data)


class MenuView(APIView):
    permission_classes = (IsAuthenticated, IsWorker)

    @swagger_auto_schema(
        operation_summary='Getting today the most rated menu by restaurant employees',
        responses=menu_get_response_body_schema
    )
    def get(self, request):
        current_day = timezone.now().date()
        restaurant_service = RestaurantService()

        current_day_menu = restaurant_service.get_top_menu_by_restaurant_and_day(request.user.restaurant, current_day)
        if not current_day_menu:
            return Response(status=HTTP_404_NOT_FOUND)

        serializer = MenuSerializer(current_day_menu)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=RestaurantSerializer,
        operation_summary='Creates a menu for a restaurant',
        responses=menu_post_response_body_schema
    )
    def post(self, request):
        request.data.update(
            {
                'created_by': request.user.pk,
                'restaurant': request.user.restaurant.pk,
                'day': timezone.now().date()
            }
        )
        serializer = MenuSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        menu = serializer.save()
        response_serializer = MenuResponseSerializer(menu)
        return Response(status=HTTP_201_CREATED, data=response_serializer.data)


class VoteView(APIView):
    permission_classes = (IsAuthenticated, IsWorker)
    versioning_class = BuildVersionScheme

    @swagger_auto_schema(
        request_body=VotesTop3Serializer,
        operation_summary='Votes for at most 3 top menus',
        responses=vote_response_body_schema
    )
    def post(self, request):
        current_day = timezone.now().date()
        vote_service = VoteService()

        with transaction.atomic():
            votes = vote_service.get_employee_votes(request.user, current_day)
            if votes:
                votes.delete()

            if request.version == settings.API_VERSION_1:
                serializer = VoteSerializer(data=request.data)
                request.data.update(
                    {
                        'voted_by': request.user.pk,
                        'score': SCORE_MAPPER[1]  # score for the 1-st place
                    }
                )
                serializer.is_valid(raise_exception=True)
                vote = serializer.save()
                response_serializer = VoteSerializer(vote)
                return Response(status=HTTP_201_CREATED, data=response_serializer.data)

            if request.version == settings.API_VERSION_2:
                input_serializer = VotesTop3Serializer(context={'request': request}, data=request.data, many=True)
                input_serializer.is_valid(raise_exception=True)
                serializer = VoteSerializer(data=input_serializer.data, many=True)
                serializer.is_valid(raise_exception=True)
                votes = serializer.save()
                response_serializer = VoteSerializer(votes, many=True)
                return Response(status=HTTP_201_CREATED, data=response_serializer.data)

            return Response(status=HTTP_400_BAD_REQUEST, data={'message': API_VERSION_NOT_SPECIFIED_MSG})


class ResultView(APIView):
    permission_classes = (IsAuthenticated, IsWorker)

    @swagger_auto_schema(
        operation_summary='Outputs all menus with summarized votes',
        responses=results_response_body_schema
    )
    def get(self, request):
        current_day = timezone.now().date()
        restaurant_service = RestaurantService()
        results = restaurant_service.get_menus_ranked_by_restaurant_and_day(request.user.restaurant, current_day)

        if not results:
            return Response(status=HTTP_404_NOT_FOUND, data={'message': RESULTS_NOT_AVAILABLE_MSG})

        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)
