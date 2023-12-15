from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from product.models import CartItem
from .forms import *
from home import verify
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate, gettext


def home(request):

    return render(request, "pages/home.html")


def about(request):
    return render(request, "pages/about.html")


def contact(request):
    return render(request, "pages/contact.html")


@login_required
def verify_code(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            if verify.check(request.user.phone_number, code):
                request.user.is_verified = True
                request.user.save()
                return redirect('accounts:profile')
            else:
                messages.error(request, "Verification is reject Try again")
    else:
        form = VerifyForm()
    return render(request, 'auth/verify.html', {'form': form})
