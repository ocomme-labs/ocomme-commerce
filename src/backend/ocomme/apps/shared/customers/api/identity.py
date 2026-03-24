from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.models import SocialAccount
from dj_rest_auth.registration.views import SocialLoginView

from dj_rest_auth.views import LoginView
from apps.shared.customers.throttles import LoginRateThrottle
from django.urls import path
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import Response

GOOGLE_PROVIDER = "google"


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client

    def post(self, request, *args, **kwargs):
        resp = super().post(request, *args, **kwargs)
        user = self.request.user
        google = SocialAccount.objects.filter(
            user=user, provider=GOOGLE_PROVIDER
        ).first()
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token

        extra = google.extra_data if google else None
        data = {
            "access_token": str(access_token),
            "refresh_token": str(refresh_token),
            "profile": extra,
        }
        return Response(data, status=resp.status_code)


class CustomLoginView(LoginView):
    throttle_classes = [LoginRateThrottle]


identity_api_urls = [
    path("login/google/", GoogleLogin.as_view(), name="api-google-login"),
    path("login/", CustomLoginView.as_view(), name="api-login-view"),
]
