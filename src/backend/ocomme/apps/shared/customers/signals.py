from django.contrib.auth.signals import user_login_failed, user_logged_in
from django.dispatch import receiver
from apps.shared.customers.models import Merchant
from django.utils import timezone
from datetime import timedelta
from django.db import transaction

LOCK_MAP = {
    5: 60,
    6: 5 * 60,
    7: 30 * 60,
    8: 2 * 60 * 60,
    9: 24 * 60 * 60,
}


@receiver(user_login_failed)
def handle_login_failed(sender, credentials, request, **kwargs):
    # Lấy email hoặc username tùy theo config của bạn
    email = credentials.get("email") or credentials.get("username")
    if not email:
        return

    now = timezone.now()

    with transaction.atomic():
        try:
            merchant = Merchant.objects.select_for_update().get(email=email)
        except Merchant.DoesNotExist:
            return

        merchant.failed_login_attempts += 1
        merchant.last_failed_login = now
        attempts = merchant.failed_login_attempts

        lock_duration = LOCK_MAP.get(attempts)

        if attempts >= 10:
            merchant.is_active = False
            merchant.is_locked = True
            merchant.locked_until = None

        elif lock_duration:
            merchant.is_locked = True
            merchant.locked_until = now + timedelta(seconds=lock_duration)

        else:
            merchant.is_locked = False
            merchant.locked_until = None

        merchant.save(
            update_fields=[
                "is_active",
                "failed_login_attempts",
                "last_failed_login",
                "is_locked",
                "locked_until",
            ]
        )


@receiver(user_logged_in)
def handle_login_success(sender, user, request, **kwargs):
    Merchant.objects.filter(email=user.email).update(
        failed_login_attempts=0,
        last_failed_login=None,
        is_locked=False,
        locked_until=None,
    )
