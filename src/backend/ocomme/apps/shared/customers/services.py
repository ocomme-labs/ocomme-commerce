"""Provide the write Model function"""

import logging
from datetime import timedelta

from apps.shared.customers.exceptions import (
    TenantCreationError,
    UserDoesNotExistError,
)
from apps.shared.customers.models import Client, Domain, Merchant
from django.db import IntegrityError, transaction
from django.utils import timezone
from django.utils.text import slugify


logger = logging.getLogger(__name__)


# TODO: Đưa xuống broker! maybelated
def create_tenant_service(
    store_name: str,
    plan_type: str,
    owner_email: str,
    paid_until: int,
) -> Client:
    """
    Service xử lý nghiệp vụ tạo Tenant và Domain.
    """
    try:
        user = Merchant.objects.get(email=owner_email)
    except Merchant.DoesNotExist as e:
        raise UserDoesNotExistError(
            f"User with email {owner_email} does not exist!"
        ) from e

    schema_name = slugify(store_name).replace("-", "")

    if Client.objects.filter(schema_name=schema_name).exists():
        raise TenantCreationError(
            "Store name results in a duplicate schema. Please try another name."
        )

    now = timezone.now()
    expired_at = now + timedelta(days=paid_until)

    try:
        with transaction.atomic():

            client = Client.objects.create(
                name=store_name,
                schema_name=schema_name,
                owner=user,
                paid_until=expired_at,
                plan_type=plan_type,
                created_by=user,
            )

            domain_name = f"{schema_name}.domain.com"
            Domain.objects.create(domain=domain_name, tenant=client, is_primary=True)

            return client

    except IntegrityError as e:
        logger.error(f"Database Integrity Error: {e}")
        raise TenantCreationError("Domain or Schema already exists.") from e

    except Exception as e:
        logger.error(f"Unexpected error during tenant creation: {e}")
        raise TenantCreationError(
            "An unexpected error occurred while creating your store."
        ) from e


class MerchantServices:

    @staticmethod
    def update_merchant_detail_service(email, extra_data):
        try:
            merchant, _ = Merchant.objects.get_or_create(email=email)

            if not merchant.name:
                merchant.name = extra_data.get("name")

            if not merchant.picture_url:
                merchant.picture_url = extra_data.get("picture")

            if merchant.name:
                merchant.is_profile_completed = True

            merchant.save(
                update_fields=[
                    "name",
                    "picture_url",
                    "is_profile_completed",
                ]
            )

            return merchant

        except Merchant.DoesNotExist as e:
            logger.error("Merchant does not exists")
            raise UserDoesNotExistError(
                f"User with email {email} does not exist!"
            ) from e

        except Exception as e:
            logger.error(f"Unexpected error during tenant creation: {e}")
            raise TenantCreationError(
                "An unexpected error occurred while creating your store."
            ) from e
