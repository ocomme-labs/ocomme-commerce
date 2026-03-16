from apps.shared.customers.models import Client
from apps.shared.customers.serializers import (
    ReadClientSerializer,
    WriteClientSerializer,
)
from apps.shared.customers.services import create_tenant_service
from common.mixins import OcommeMixinApiView
from rest_framework import permissions, serializers
from rest_framework.views import Response

# from dj_rest_auth.registration.views import SocialLoginView

MODIFY_METHOD = ["POST", "PUT", "PATCH"]


# TODO: PUT, DELETE method
class ClientAPIView(OcommeMixinApiView):
    queryset = Client.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in MODIFY_METHOD:
            return WriteClientSerializer
        return ReadClientSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response({"MESSAGE": "Data is empty!"}, 400)
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)

        read_serializer = ReadClientSerializer(instance)
        header = self.get_success_headers(read_serializer)

        return Response(
            {
                "MESSAGE": "SUCCESSFULLY",
                "DATA": read_serializer.data,
            },
            status=201,
            headers=header,
        )

    def perform_create(self, serializer):
        try:
            data = serializer.validated_data
            return create_tenant_service(
                owner_email=self.request.user.email,
                store_name=data.get("store_name"),
                plan_type=data.get("plan_type"),
                paid_until=data.get("paid_until"),
            )
        except Exception as e:
            raise serializers.ValidationError({"detail": str(e)}) from e

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
