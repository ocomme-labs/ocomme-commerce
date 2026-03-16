from apps.shared.customers.models import Client
from common.models import PlanTypeEnum
from django.utils.text import slugify
from rest_framework import serializers


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
