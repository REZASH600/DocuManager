from django.db import models
from django.utils.translation import gettext_lazy as _

class Participant(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", _("Active")
        IN_PROGRESS = "in_progress", _("In Progress")
        NOT_ACTIVE = "not_active", _("Not Active")

    first_name = models.CharField(max_length=255, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=255, verbose_name=_("Last Name"))
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        verbose_name=_("Status"),
    )

    class Meta:
        verbose_name = _("Participant")
        verbose_name_plural = _("Participants")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
