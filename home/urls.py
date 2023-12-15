from django.urls import path
from home import views

app_name = "home"

urlpatterns = [
    path('', views.home, name="home"),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('verify/', views.verify_code, name="verify"),
]
