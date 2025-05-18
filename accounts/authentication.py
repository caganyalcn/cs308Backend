from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from accounts.models import User

class CustomSessionAuthentication(BaseAuthentication):
    

    def authenticate(self, request):
        user_id = request.session.get("user_id")
        if not user_id:
            return None  # oturum yok → Anonymous

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("User not found")

        return (user, None)
