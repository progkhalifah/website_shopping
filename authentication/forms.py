from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, PasswordResetForm
from .models import CustomUser


class UserCreationForm(BaseUserCreationForm):
    phone_number = forms.CharField(max_length=20, required=True, help_text='Phone number')

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'phone_number', 'password1', 'password2')


# class PasswordResetForm(PasswordResetForm):
#     def __init__(self, *args, **kwargs):
#         super(PasswordResetForm, self).__init__(*args, **kwargs)
