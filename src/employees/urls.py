from django.urls import path
from employees.views import EmployeeView, TokenView


app_name = 'employee'


urlpatterns = [
    path('signup', EmployeeView.as_view(), name='signup'),
    path('token', TokenView.as_view(), name='token'),
]
