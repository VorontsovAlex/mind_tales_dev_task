from employees.models import Employee


class EmployeeService:
    def signup(self, **kwargs):
        employee = Employee.objects.create_user(**kwargs)
        return employee
