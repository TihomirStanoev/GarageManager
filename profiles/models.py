from django.core.validators import RegexValidator
from django.db import models
from common.models import TimeStampedModel
from profiles.validators import PhoneNumberValidator


class Profile(TimeStampedModel):
    first_name = models.CharField(
        max_length=20
    )

    last_name = models.CharField(
        max_length=20
    )

    email = models.EmailField(
        unique=True
    )

    phone_number = models.CharField(
        max_length=15,
        validators=[PhoneNumberValidator()],
        unique=True
    )

    class Meta:
        ordering = ['first_name', 'last_name']


    def __str__(self):
        return f'{self.first_name} {self.last_name}'





