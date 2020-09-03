from django.contrib.auth.models import User


class EmailAuthBackend(object):
    """
    Authenticate using an email address.Custom authentication using email.In built in authentication using username and password.
    """
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username) # retrieve a user with the given email address
            if user.check_password(password): # for password checking
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id): # get a user through the ID set in the user_id
        try:
            # django uses the backend that authenticated the user to retrieve the user object for the duration of the user session
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None