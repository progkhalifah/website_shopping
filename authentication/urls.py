from django.urls import path
from authentication import views
from django.conf.urls.static import static

app_name = "accounts"

urlpatterns = [
    path('login/', views.custom_login, name="login"),
    path('register/', views.custom_register, name="register"),
    path('signout/', views.custom_signout, name="signout"),
    path('profile/', views.custom_profile, name="profile"),
    path('password_change/', views.password_change, name="password_change"),

]
