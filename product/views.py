from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate, gettext
from django.contrib import messages
from authentication.models import CustomUser
from product.models import *


def shop(request):
    # products = Products_shop.objects.all()
    available_colors = Color_product.objects.all()
    available_sizes = Size_product.objects.all()
    # Get the selected color choices from the query parameters
    selected_colors = request.GET.getlist('color')
    selected_size = request.GET.getlist('size')

    # Filter products based on selected colors
    if selected_colors:
        products = Products_shop.objects.filter(colors__id__in=selected_colors)
    else:
        products = Products_shop.objects.all()





    # size_ids = request.GET.getlist("sizes")
    # if size_ids:
    #     products = products.filter(size__in=size_ids)



    context = {
        "productshops": products,
        'available_colors': available_colors,
        'selected_colors': selected_colors,


    }
    return render(request, "pages/shop.html", context)


def single_shop(request, id_support_product):
    productt = Products_shop.objects.get(id_support_product=id_support_product)
    color_prod = Color_product.objects.filter(products_shop=id_support_product)
    size_prod = Size_product.objects.filter(products_shop=id_support_product)
    user = request.user

    # define variables
    product_name = request.POST.get("product_name")
    product_desc = request.POST.get("product_describe")
    product_price = request.POST.get("product_price")
    product_color = request.POST.get("product_color")
    product_size = request.POST.get("product_size")
    product_quantity = request.POST.get("product_quantity")


    # end

    if request.method == "POST":
        if "btn_add_item" in request.POST:
            # # Retrieve the product instance based on the product name
            # try:
            #     product_instance = Products_shop.objects.get(name=product_name)
            # except Products_shop.DoesNotExist:
            #     # Handle the case when the product doesn't exist
            #     messages.error(request, "Product not found.")
            try:
                if user is not None:
                    CartItem.objects.create(
                        user=user,
                        product_name=product_name,
                        color=product_color,
                        size=product_size,
                        price=product_price,
                        quantity=product_quantity
                    )

                    messages.success(request, "Item added to card")
                else:
                    raise Exception("Raise : Item doesn't add to card")
            except BaseException as ex:
                messages.error(request, "There is something wrong when you click on create without choose color or size or quantity")
                print("Error message is : ", ex)
        else:
            messages.error(request, "There is something wrong with add items")

    context = {
        "productshop": productt,
        "colorshop": color_prod,
        "sizeshop": size_prod,
        "user_id": user
    }
    return render(request, "pages/shop-single.html", context)

# def add_item_product(request, product_id):
#     product = Products_shop.objects.get(id_support_product=product_id)
#     cart = request.session.get('cart', {})
#
#     if product_id in cart:
#         cart[product_id]['quantity'] += 1
#     else:
#         cart[product_id] = {
#             'name': product.name_product,
#             'price': product.price_product,
#             'quantity': 1
#         }
#


# from django.shortcuts import render
#
# def my_view(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')  # Retrieve the 'name' input value
#         email = request.POST.get('email')  # Retrieve the 'email' input value
#
#         # Process the data as needed
#         print(f"Name: {name}, Email: {email}")
# 
#     return render(request, 'my_template.html')
