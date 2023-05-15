from rest_framework.permissions import BasePermission
from employees.enums import EmployeeGroup


class IsWorker(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name=EmployeeGroup.WORKER):
            return True
        return False


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name=EmployeeGroup.ADMIN):
            return True
        return False
