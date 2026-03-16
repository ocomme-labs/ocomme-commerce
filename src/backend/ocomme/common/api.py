from django.urls import path
from django.urls.resolvers import URLPattern
from rest_framework.views import APIView, Response


class HealCheck(APIView):
    def get(self, request, *args, **kwargs) -> Response:
        return Response(data={"MESSAGE": "HEALTHY"}, status=200)


common_urls_pattern: list[URLPattern] = [
    path("", HealCheck.as_view(), name="api-heal-check"),
]
