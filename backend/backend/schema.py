from drf_spectacular.contrib.rest_framework_simplejwt import SimpleJWTScheme


class SafeJWTAuthenticationScheme(SimpleJWTScheme):
    target_class = 'home.authentication.SafeJWTAuthentication'  # full import path OR class ref
    name = 'SafeJWTAuthentication'