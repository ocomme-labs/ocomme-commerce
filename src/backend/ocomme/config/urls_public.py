"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import apps.shared.customers.api.identity as identity_urls
import apps.shared.customers.api.views as customer_urls
import common.api as common
from dj_rest_auth.views import PasswordResetConfirmView
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # -------------------------
    # Authentication: Default (dj-rest-auth)
    # -------------------------
    path("auth/", include("dj_rest_auth.urls")),
    path(
        "auth/confirm-reset-password/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    # Registration
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    # Google OAuth TESTING
    path("accounts/", include("allauth.urls")),
    path("auth/identity/", include(identity_urls.identity_api_urls)),
    # ----- App Urls -----
    # Health checking
    path("health/", include(common.common_urls_pattern)),
    path(
        "api/",
        include(
            [
                path("", include(customer_urls.customers_api_urls)),
            ]
        ),
    ),
]
