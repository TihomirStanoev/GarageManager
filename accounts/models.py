from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts.managers import CustomUserManager
from accounts.validators import PhoneNumberValidator


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=15,
        validators=[PhoneNumberValidator()],
        unique=True,
    )


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    objects = CustomUserManager()

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email

    @property
    def profile_with_phone(self):
        return f'{self.first_name} {self.last_name} ({self.phone_number})'