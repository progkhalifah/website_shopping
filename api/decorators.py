from functools import wraps

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.models import CustomUser
from product.models import *


def registration_validate(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        errors = {}

        # Validate 'first_name' and 'last_name' fields are present
        if 'first_name' not in request.data:
            errors['first_name'] = "This field is required."
        if 'last_name' not in request.data:
            errors['last_name'] = "This field is required."

        # Validate that the 'username' field is present in the request data
        if 'username' not in request.data:
            errors['username'] = 'This field is required.'
        else:
            if CustomUser.objects.filter(username=request.data['username']).exists():
                errors['username'] = "This username is already in use"

        # Validate that the 'username' field is at least 3 characters long
        if 'username' in request.data and len(request.data['username']) < 3:
            errors['username'] = 'This field must be at least 3 characters long.'

            # Validate 'email' field is present
        if 'email' not in request.data:
            errors['email'] = "This field is required."
        else:
            if CustomUser.objects.filter(email=request.data["email"]).exists():
                errors["email"] = "This email is already in use"

            # Validate 'phone_number' field is present
        if 'phone_number' not in request.data:
            errors['phone_number'] = "This field is required."

        # Validate 'password1' and 'password2' fields are present
        if 'password' not in request.data:
            errors['password'] = "This field is required."
        else:
            # Check if the password meets the strength requirements
            password = request.data['password']
            if not (
                    any(c.islower() for c in password) and  # Contains lowercase
                    any(c.isupper() for c in password) and  # Contains uppercase
                    any(c.isdigit() for c in password) and  # Contains a digit
                    any(c in r'!@#$%^&*()-_=+[]{}|;:,.<>?/~`' for c in password)  # Contains a special character
            ):
                errors['password'] = 'Password must contain lowercase, uppercase, digit, and special character.'

        if not errors:
            return view_func(request, *args, **kwargs)  # Indicate valid data

        # Raise a validation error with the collected error messages
        raise ValidationError(errors)

    return wrapper


def verification_required(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.user

        if user.is_verified:
            return view_func(request, *args, **kwargs)
        else:
            response_data = {
                "status": "Failed",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "You have to verify your account"
            }
            return Response(response_data, status.HTTP_400_BAD_REQUEST, content_type="application/json")

    return wrapper


def verify_validate(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        errors = {}

        # Validate 'first_name' and 'last_name' fields are present
        if 'code' not in request.data:
            errors['code'] = "This field is required."

        if not errors:
            return view_func(request, *args, **kwargs)  # Indicate valid data

        # Raise a validation error with the collected error messages
        raise ValidationError(errors)

    return wrapper


def cart_item_validate(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        errors = {}

        # Validate 'first_name' and 'last_name' fields are present
        if 'user' not in request.data:
            errors['user'] = "This field is required."

        if 'product_name' not in request.data:
            errors['product_name'] = "This field is required."

        if 'price' not in request.data:
            errors['price'] = "This field is required."

        if 'price' not in request.data:
            errors['price'] = "This field is required."

        if not errors:
            return view_func(request, *args, **kwargs)  # Indicate valid data

        # Raise a validation error with the collected error messages
        raise ValidationError(errors)

    return wrapper


def order_validate(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        errors = {}

        # Validate 'first_name' and 'last_name' fields are present
        if 'user' not in request.data:
            errors['user'] = "This field is required."

        if 'product_name' not in request.data:
            errors['product_name'] = "This field is required."

        if 'price' not in request.data:
            errors['price'] = "This field is required."

        if 'status' not in request.data:
            errors['status'] = "This field is required."

        if not errors:
            return view_func(request, *args, **kwargs)  # Indicate valid data

        # Raise a validation error with the collected error messages
        raise ValidationError(errors)

    return wrapper
