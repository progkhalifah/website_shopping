"""
URL configuration for django9onlinestore_edit project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from django9onlinestore_edit import settings

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('admin/', admin.site.urls),
    path('', include('home.urls', namespace="home_en")),
    path('shop/', include('product.urls', namespace="product_en")),
    path('card/', include('card.urls', namespace="card_en")),
    path('accounts/', include('authentication.urls', namespace="auth_en")),
    path('api/', include('api.urls', namespace="api_en")),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="auth/reset_password.html"), name='reset_password'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name="auth/password_reset_done.html"), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(

    path('', include('home.urls', namespace="home_ar")),
    path('shop/', include('product.urls', namespace="product_ar")),
    path('card/', include('card.urls', namespace="card_ar")),
    path('accounts/', include('authentication.urls', namespace="auth_ar")),

)