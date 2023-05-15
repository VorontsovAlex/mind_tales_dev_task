from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


SchemaView = get_schema_view(
   openapi.Info(
      title='Mind Tales Dev Task API',
      default_version=settings.API_VERSION_2
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('employee/', include('employees.urls', namespace='auth')),
    path('restaurant/', include('restaurant.urls', namespace='restaurant')),
    re_path(r'swagger/$', SchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]
