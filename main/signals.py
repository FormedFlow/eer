from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Student


def student_register(sender, **kwargs):
    if kwargs['created']:
        Student.objects.create(user=kwargs['instance'])
