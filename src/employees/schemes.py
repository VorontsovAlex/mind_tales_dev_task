from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from drf_yasg import openapi


signup_request_body_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'login': openapi.Schema(type=openapi.TYPE_STRING, description='Login'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
        'restaurant': openapi.Schema(type=openapi.TYPE_INTEGER, description='Restaurant ID'),
    },
    required=['login', 'password']
)

signup_response_body_schema = {
    HTTP_201_CREATED: openapi.Response(
        description='Employee created successfully',
        examples={
            'application/json': {
                'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
            }
        }
    ),
    HTTP_400_BAD_REQUEST: openapi.Response(
        description='Failed to create employee',
        examples={
            'application/json': {
                'login': [
                    'Employee with this Login already exists.'
                ]
            }
        }
    ),
    HTTP_401_UNAUTHORIZED: openapi.Response(
        description='Authorization Required',
        examples={
            'application/json': {
                'detail': 'Authentication credentials were not provided.'
            }
        }
    ),

    HTTP_403_FORBIDDEN: openapi.Response(
        description='Forbidden to create employee',
        examples={
            'application/json': {
                'detail': 'You do not have permission to perform this action.'
            }
        }
    ),

}
