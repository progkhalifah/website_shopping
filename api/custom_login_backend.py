from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.utils import timezone


class CustomLoginBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        CustomUser = get_user_model()

        if "@" in username:
            user = CustomUser.objects.filter(email=username).first()
        elif "+" in username:
            user = CustomUser.objects.filter(phone_number=username).first()
        else:
            user = CustomUser.objects.filter(username=username).first()

        if user and user.check_password(password):
            user.last_login = timezone.now()
            user.save()
            return user

        return None
