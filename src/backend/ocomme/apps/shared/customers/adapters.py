from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from apps.shared.customers.services import MerchantServices


class CustomDefaultSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        extra_data = sociallogin.account.extra_data or {}
        MerchantServices.update_merchant_detail_service(
            email=user.email, extra_data=extra_data
        )
        return user
