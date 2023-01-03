from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class TransactionStatusTypes(TextChoices):
    PENDING = "Pending", _("Pending"),
    COMPLETE = "Complete", _("Complete"),
    FAILED = "Failed", _("Failed")

class TransactionTypes(TextChoices):
    DEBIT = "Debit", _("Debit"),
    CREDIT = "Credit", _("Credit")
