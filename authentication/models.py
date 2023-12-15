from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class CustomUser(AbstractUser, PermissionsMixin):
    phone_number = models.TextField(default="00966123456789", max_length=20, blank=False,
                                    help_text="Enter Your Phone Number",
                                    error_messages="You have to enter your phone number",
                                    null=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
