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

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        db_table = "users"

        indexes = [
            models.Index(fields=['email', 'password'], name='email_password_idx'),
            models.Index(fields=['last_name', 'first_name'], name='last_name_first_name_idx'),
            models.Index(fields=['first_name'], name='first_name_idx'),
        ]

    def __str__(self):
        return self.email