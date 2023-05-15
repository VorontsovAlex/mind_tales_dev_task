from django.db.models import TextChoices


class EmployeeGroup(TextChoices):
    ADMIN = 'Administrator'
    WORKER = 'Worker'

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
