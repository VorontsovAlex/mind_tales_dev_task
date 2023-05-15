from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from employees.models import Employee
from employees.enums import EmployeeGroup


class TokenObtainPairSerializerCustom(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['token'] = str(refresh.access_token)
        return data


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['login', 'password', 'restaurant']

    def validate(self, attrs):
        if not attrs.get('restaurant') and self.context['role'] == EmployeeGroup.WORKER:
            raise ValidationError('For the role Worker restaurant must be specified')

        if attrs.get('restaurant') and self.context['role'] == EmployeeGroup.ADMIN:
            raise ValidationError('For the role Administrator restaurant must not be specified')

        return attrs


class EmployeeRoleSerializer(serializers.Serializer):
    role = serializers.CharField()

    def validate(self, attrs):
        if not EmployeeGroup.has_value(attrs['role']):
            raise ValidationError('Role not exist in available employees groups')

        return attrs
