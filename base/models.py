from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from django.utils import timezone

class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-managed `id`, `is_deleted`, `created_at` and
    `modified_at` fields.
    """
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name="Public Identifier")
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    is_deleted = models.BooleanField(default=False)
    modified_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True