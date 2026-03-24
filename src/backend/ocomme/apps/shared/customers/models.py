from common.models import BaseModel, PlanTypeEnum
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django_tenants.models import DomainMixin, TenantMixin
from phonenumber_field.modelfields import PhoneNumberField


class Client(TenantMixin, BaseModel):
    """Provided Tenant models"""

    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    paid_until = models.DateTimeField()
    is_trial = models.BooleanField(default=False)
    plan_type = models.CharField(
        max_length=18,
        choices=PlanTypeEnum.choices,
        default=PlanTypeEnum.FREE,
    )

    def __str__(self):
        return self.schema_name


class Domain(DomainMixin):
    pass


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email must required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must be active")

        return self._create_user(email, password, **extra_fields)


class Merchant(AbstractBaseUser, PermissionsMixin, BaseModel):

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=208, blank=True, null=True)
    picture_url = models.CharField(max_length=500, blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    # address = models.ForeinKey(Address, blank=True, null=True)  # TODO: Update Address models
    is_profile_completed = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    is_locked = models.BooleanField(default=False)
    locked_until = models.DateTimeField(null=True, blank=True)
    failed_login_attempts = models.IntegerField(default=0)
    last_failed_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email}"
