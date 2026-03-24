from apps.shared.customers.models import Client, Merchant
from common.models import PlanTypeEnum
from django.utils.text import slugify
from rest_framework import serializers
from dj_rest_auth.serializers import LoginSerializer
from django.utils import timezone


class CustomLoginSerializer(LoginSerializer):

    def get_auth_user(self, username, email, password):
        now = timezone.now()
        try:
            merchant = Merchant.objects.get(email=email)
        except Merchant.DoesNotExist:
            raise serializers.ValidationError({"ERROR": "Invalid credentials"})

        if merchant.is_locked and merchant.locked_until and merchant.locked_until < now:
            merchant.is_locked = False
            merchant.locked_until = None
            merchant.save(update_fields=["is_locked", "locked_until"])

        if not merchant.is_active:
            raise serializers.ValidationError(
                {
                    "error_code": "ACCOUNT_DISABLED",
                    "detail": {
                        "title": "Account Permanently Locked",
                        "message": "Your account has been disabled due to multiple security violations. Please contact the System Administrator for assistance.",
                        "contact_support": "admin@yourdomain.com",
                    },
                }
            )

        if merchant.is_locked:
            raise serializers.ValidationError(
                {
                    "error_code": "ACCOUNT_TEMPORARILY_LOCKED",
                    "detail": {
                        "title": "Account is locked",
                        "message": f"Too many failed attempts. Please try again after {merchant.locked_until}.",
                        "locked_until": merchant.locked_until,
                    },
                }
            )

        return super().get_auth_user(username, email, password)


class ReadClientSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source="name")

    class Meta:
        model = Client
        fields = [
            "id",
            "store_name",
            "schema_name",
            "plan_type",
            "paid_until",
            "created_at",
        ]


class WriteClientSerializer(serializers.Serializer):
    store_name = serializers.CharField(max_length=208)
    plan_type = serializers.ChoiceField(choices=PlanTypeEnum.choices, required=False)
    paid_until = serializers.IntegerField()

    def validate(self, attrs):
        store_name = attrs.get("store_name")
        schema_name = slugify(store_name).replace("-", "")

        if Client.objects.filter(schema_name=schema_name).exists():
            raise serializers.ValidationError(
                {
                    "MESSAGE": "Store name results in a duplicate schema. "
                    "Please try another name."
                }
            )
        return attrs


class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = [
            "id",
            "email",
            "name",
            "phone",
            "picture_url",
            "is_profile_completed",
            "is_locked",
        ]
