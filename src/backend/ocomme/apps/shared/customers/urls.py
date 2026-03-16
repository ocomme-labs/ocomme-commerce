from apps.shared.customers.api.views import ClientAPIView
from django.urls import path

urlpatterns = [
    path("client/", ClientAPIView.as_view(), name="api-client"),
]
