from django.urls import path
from card import views

app_name = "card"

urlpatterns = [
    path('cart', views.cart, name="cart"),
    path('delete_item_card/<pk>/', views.delete_item_card, name="delete_item_card"),
    path('edit_item_card/', views.edit_item_card, name="edit_item_card"),
    path('add_order', views.add_order, name="add_order"),
    path('checkout/', views.check_out, name="checkout"),
    path('successfully/', views.successfully, name="successfully"),
    path('export_pdf/', views.export_pdf, name="export_pdf"),

]
