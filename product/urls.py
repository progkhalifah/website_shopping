from django.urls import path
from product import views
from django.conf.urls.static import static

app_name = "product"

urlpatterns = [
    path('', views.shop, name="shop"),
    path('single_shop/<uuid:id_support_product>/', views.single_shop, name="single_shop"),
]
