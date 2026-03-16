from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.urls import path
from rest_framework_simplejwt.tokens import RefreshToken

GOOGLE_PROVIDER = "google"


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    # callback_url = "http://localhost:8000"

    def get_response(self):
        response = super().get_response()

        user = self.user
        refresh = RefreshToken.for_user(user)

        response.data["access"] = str(refresh.access_token)
        response.data["refresh"] = str(refresh)

        return response


api_identity_urls = [
    path("", GoogleLogin.as_view(), name="api-google-login"),
]
