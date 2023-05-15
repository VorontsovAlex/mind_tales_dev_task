from rest_framework import versioning


class BuildVersionScheme(versioning.BaseVersioning):
    def determine_version(self, request, *args, **kwargs):
        return request.META.get('HTTP_BUILD_VERSION', None)
