from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from drf_yasg import openapi


restaurant_response_body_schema = {
    HTTP_201_CREATED: openapi.Response(
        description='Restaurant created successfully',
        examples={
            'application/json': {
                'id': 3,
                'address': 'adress_5'
            }
        }
    ),
    HTTP_400_BAD_REQUEST: openapi.Response(
        description='Creating restaurant failed',
        examples={
            'application/json': {
                'address': [
                    'Restaurant with this Address already exists.'
                ]
            }
        }
    ),
}


menu_get_response_body_schema = {
    HTTP_200_OK: openapi.Response(
        description='Menu is available',
        examples={
            'application/json': {
                'name': 'menu_3',
                'data': 'data_3',
                'restaurant': 1,
                'day': '2023-05-14',
                'created_by': 2
            }
        }

    ),
    HTTP_404_NOT_FOUND: openapi.Response(
        description='No menu found for today',
        examples={'application/json': {}}
    ),
}


menu_post_response_body_schema = {
    HTTP_201_CREATED: openapi.Response(
        description='Menu created successfully',
        examples={
            'application/json': {
                'name': 'menu_3',
                'data': 'data_3',
                'restaurant': 1,
                'day': '2023-05-14',
                'created_by': 2
            }
        }
    ),

    HTTP_400_BAD_REQUEST: openapi.Response(
        description='Creating menu failed',
        examples={
            'application/json': {
                'data': [
                    'This field is required.'
                ]
            }
        }
    ),
}


vote_response_body_schema = {
    HTTP_201_CREATED: openapi.Response(
        description='Votes are submitted successfully',
        examples={
            'application/json': [
                {
                    'menu': 7,
                    'score': 3,
                    'voted_by': 3
                },
                {
                    'menu': 8,
                    'score': 2,
                    'voted_by': 3
                }
            ]
        }
    ),

    HTTP_400_BAD_REQUEST: openapi.Response(
        description='Failed to submit votes',
        examples={
            'application/json': [
                {
                    'non_field_errors': [
                        'Invalid place value. Must be range from 1 to 3'
                    ]
                },
                {}
            ]
        }
    ),

}


results_response_body_schema = {
    HTTP_200_OK: openapi.Response(
        description='Results are available',
        examples={
            'application/json': [
                {
                    'menu': 7,
                    'score': 3,
                    'voted_by': 3
                },
                {
                    'menu': 8,
                    'score': 2,
                    'voted_by': 3
                }
            ]
        }
    ),

    HTTP_404_NOT_FOUND: openapi.Response(
        description='Results not available',
        examples={
            'application/json': {
                'message': 'Results not available; Either no menu uploaded yet or no votes are given to any menus'
            }
        }
    ),
}
