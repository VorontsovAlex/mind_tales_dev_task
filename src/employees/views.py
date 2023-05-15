from django.contrib.auth.models import Group
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from app.permissions import IsAdmin
from employees.schemes import signup_request_body_schema, signup_response_body_schema
from employees.serializers import EmployeeRoleSerializer, EmployeeSerializer, TokenObtainPairSerializerCustom
from employees.services import EmployeeService


class TokenView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializerCustom


class EmployeeView(APIView):
    permission_classes = (IsAuthenticated, IsAdmin)

    @swagger_auto_schema(
        request_body=signup_request_body_schema,
        operation_summary='Signing up Employee',
        responses=signup_response_body_schema
    )
    def post(self, request):
        role_serializer = EmployeeRoleSerializer(data={'role': request.data.pop('role', None)})
        role_serializer.is_valid(raise_exception=True)

        serializer = EmployeeSerializer(data=request.data, context={'role': role_serializer.data['role']})
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            employee_service = EmployeeService()
            employee = employee_service.signup(**serializer.validated_data)
            employee.groups.add(Group.objects.get(name=role_serializer.data['role']))

        return Response(status=HTTP_201_CREATED, data={'employee': employee.id})
