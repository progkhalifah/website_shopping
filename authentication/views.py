from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .forms import *
from home import verify
from home.decorators import verification_required
from .forms import PasswordResetForm
from django.db.models.query_utils import Q


# Create your views here.

def custom_login(request):
    username = request.POST.get("auth_username")
    password = request.POST.get("auth_password")

    if request.method == "POST":
        if "btn_login" in request.POST:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login Successfully")
                print(f"{messages.success(request, 'Login Successfully')}")
                return redirect("accounts:profile")
            else:
                messages.error(request, "You enter wrong Username or Passowrd")
    else:
        messages.error(request, "You enter wrong Username or Passowrd")

    context = {
        'title': 'login Page',
    }
    return render(request, "auth/login.html", context)


def custom_register(request):
    try:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            print("Please Help")
            if form.is_valid():
                print("Please Help I am after form valid")
                form.save()
                verify.send(form.cleaned_data.get('phone_number'))
                return redirect('home:verify')
        else:
            print("Please Help I am after ELSE")
            messages.error(request, "Wrong Register")
            form = UserCreationForm()
            print("Please Help I am in the end")
    except Exception as e:
        print("Please help" + " " + f"{e}")

    return render(request, "auth/register.html", {'form': form})


@login_required
@verification_required
def custom_profile(request):
    return render(request, "auth/profile.html")


def custom_signout(request):
    logout(request)
    return redirect("accounts:login")


@login_required
def password_change(request):
    if request.method == "POST":
        new_password = request.POST.get("NewPassword")
        confirm_password = request.POST.get("confirmPassword")

        if new_password == confirm_password:
            user = request.user
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed Successfully")
            return redirect("accounts:profile")
        else:
            messages.error(request, "Password do not match")

    return render(request, "auth/password_change.html")


# def password_reset_request(request):
#     if request.method == "POST":
#         form = PasswordResetForm(request.POST)
#         if form.is_valid():
#             user_email = form.cleaned_data['email']
#             associated_user = get_user_model().objects.filter(email=user_email).first()
#             if associated_user:
#                 subject = "Password Reset request"
#                 message = render_to_string("auth/template_reset_password.html", {
#                     'user': associated_user,
#                     'domain': get_current_site(request).domain,
#                     'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
#                     'token': default_token_generator.make_token(associated_user),
#                     "protocol": 'https' if request.is_secure() else 'http'
#                 })
#                 email = EmailMessage(subject, message, to=[associated_user.email])
#                 if email.send():
#                     messages.success(request, "Password reset email has been sent. Check your inbox.")
#                 else:
#                     messages.error(request, "There was a problem sending the password reset email. Please try again later.")
#
#                 return redirect('home:home')
#
#     else:
#         form = PasswordResetForm()
#
#     context = {"form": form}
#     return render(request, "auth/reset_password.html", context)
#
#
# @login_required
# def passwordResetConfirm(request, uidb64, token):
#     return redirect("home:home")
