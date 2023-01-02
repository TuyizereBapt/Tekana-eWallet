from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from .managers import UserManager
from base.models import TimeStampedModel


class AuthUser(AbstractUser, TimeStampedModel):
    """
    Users within the Django authentication system are represented by this
    model.

    Email and password are required. Other fields are optional.
    """
    username = None
    email = models.EmailField(_("email address"), blank=False, unique=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, blank=False)
    verified = models.BooleanField(_("verified"), default=False)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email