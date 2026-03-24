from rest_framework.throttling import SimpleRateThrottle


class LoginRateThrottle(SimpleRateThrottle):
    scope = "login_attempts"

    def get_cache_key(self, request, view):
        ident = request.data.get("email")

        if not ident:
            ident = self.get_ident(request)

        return self.cache_format % {"scope": self.scope, "ident": ident}
