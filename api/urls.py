from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenObtainPairView

from api import views
from django.conf.urls.static import static

app_name = "api"

urlpatterns = [

    # Tokens JWT
    # path('auth/token', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    # Auth User
    path('auth/register/', views.register_user, name='register_user'),
    path('auth/verify/', views.verify_code, name='verify_user'),

    path('auth/profile/', views.get_user_profile, name='get_user_profile'),


    # Products
    path('products/all/', views.get_all_products, name='get_all_products'),
    path('products/<uuid:id>/', views.get_one_product, name='get_all_products'),

    # Card Item
    path('carditems/', views.get_items_of_card, name='get_items_of_card'),
    path('add/carditem/', views.add_items_to_card, name='add_items_to_card'),
    path('edit/carditem/<int:id>/', views.edit_items_card, name='edit_items_card'),
    path('delete/carditem/<int:id>/', views.delete_item_card, name='delete_item_card'),


    # Order
    path('add/order/', views.add_order, name='add_order'),
    path('order/', views.get_all_order, name='get_all_order'),



]


