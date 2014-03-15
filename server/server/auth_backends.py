"""
Authentication Backends
"""
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class CaseInsensitiveModelBackend(ModelBackend):
    """
    A more natural authentication backend

    By default ModelBackend does case _sensitive_ username authentication,
    which isn't what is generally expected.  This backend supports case
    insensitive username authentication.
    http://blog.shopfiber.com/?p=220
    """
    def authenticate(self, username=None, password=None):
        """
        The only difference from django's version
        """
        try:
            username = username.lower()
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
            else:
                return None
        except User.DoesNotExist:
            return None
