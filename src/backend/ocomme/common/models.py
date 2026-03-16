"""This model to create BaseModel abtract"""

import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    """
    Provides UUID primary key, created/updated timestamps,
    and tracking fields for the user who created or last modified the record
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        editable=False,
        verbose_name=_("Created at"),
        help_text=_("Timestamp when record was created"),
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created",
        verbose_name=_("Created by"),
        help_text=_("User who created this record"),
        null=True,
        blank=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        db_index=True,
        editable=False,
        verbose_name=_("Updated at"),
        help_text=_("Timestamp when record was last updated"),
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated",
        verbose_name=_("Updated by"),
        help_text=_("User who last updated this record"),
        null=True,
        blank=True,
    )
    is_delete = models.BooleanField(default=False)

    class Meta:
        abstract = True
        get_latest_by = "created_at"
        ordering = ("-created_at",)


class PlanTypeEnum(models.TextChoices):
    FREE = "free", _("Free")
    PRO = "pro", _("Pro")
