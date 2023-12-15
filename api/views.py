from django.db import transaction
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.decorators import *
from api.serializers import *
from home import verify


# Create your views here.

@api_view(["POST"])
@registration_validate  # Assuming 'registration_validate' is a custom decorator
def register_user(request):
    if request.method == "POST":
        serializer = UserSerializer(data=request.data)
        try:
            if serializer.is_valid():  # Corrected the condition
                serializer.save()
                verify.send(serializer.validated_data.get("phone_number"))
                response_data = {
                    "status": "ok",
                    "code": status.HTTP_201_CREATED,
                    "total": len(serializer.data),
                    "message": "User Created successfully",
                    "data": serializer.data
                }
                return Response(response_data, status.HTTP_201_CREATED, content_type="application/json")
            else:
                # Handle the case where the serializer is not valid
                response_data = {
                    "status": "Failed",
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Invalid data provided",
                    "errors": serializer.errors
                }
                return Response(response_data, status.HTTP_400_BAD_REQUEST, content_type="application/json")
        except Exception as e:
            response_data = {
                "status": "Failed",
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": f"There is something wrong: {str(e)}"
            }
            return Response(response_data, status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="application/json")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def verify_code(request):
    if request.method == "POST":
        try:
            serializer = VerifySerializer(data=request.data)
            if serializer.is_valid():
                code = serializer.validated_data.get("code")
                if verify.check(request.user.phone_number, code):
                    request.user.is_verified = True
                    request.user.save()
                    response_data = {
                        "status": "ok",
                        "code": status.HTTP_200_OK,
                        "total": len(serializer.data),
                        "message": "Verified Successfully",
                    }
                    return Response(response_data, status.HTTP_200_OK, content_type="application/json")
                else:
                    response_data = {
                        "status": "Failed",
                        "code": status.HTTP_400_BAD_REQUEST,
                        "message": "Verification is reject. Try again."
                    }
                    return Response(response_data, status.HTTP_400_BAD_REQUEST, content_type="application/json")
            else:
                # Serializer is not valid, return validation errors
                response_data = {
                    "status": "Failed",
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Invalid data provided",
                    "errors": serializer.errors
                }
                return Response(response_data, status.HTTP_400_BAD_REQUEST, content_type="application/json")
        except Exception as e:
            response_data = {
                "status": "Failed",
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": f"There is something wrong: {str(e)}"
            }
            return Response(response_data, status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="application/json")

    # Add a default response outside of the try-except block
    response_data = {
        "status": "Failed",
        "code": status.HTTP_200_OK,
        "message": "OK."
    }
    return Response(response_data, status.HTTP_200_OK, content_type="application/json")


########################################################################################################################

#################################### Section of Profile ###################################################################

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@verification_required
def get_user_profile(request):
    user = request.user
    if request.method == "GET":
        try:
            serializer = GetUserSerializer(user)
            response_data = {
                "status": "ok",
                "code": status.HTTP_200_OK,
                "total": len(serializer.data),
                "data": serializer.data
            }
            return Response(response_data, status.HTTP_200_OK, content_type="application/json")
        except Exception as e:
            response_data = {
                "status": "Failed",
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": f"There is something wrong: {str(e)}"
            }
            return Response(response_data, status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="application/json")


#################################### END Section of Profile ###############################################################


#################################### Section of Products ###################################################################

@api_view(['GET'])
@permission_classes([AllowAny, ])
def get_all_products(request):
    if request.method == "GET":
        try:
            all_products = Products_shop.objects.all()
            serializer = ProductSerializer(all_products, many=True)
            response_data = {
                "status": "ok",
                "code": status.HTTP_200_OK,
                "total": len(serializer.data),
                "data": serializer.data
            }
            return Response(response_data, status.HTTP_200_OK, content_type="application/json")
        except Exception as e:
            response_data = {
                "status": "Failed",
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": f"There is something wrong: {str(e)}"
            }
            return Response(response_data, status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="application/json")
    else:
        response_data = {
            "status": "Failed",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Be Sure You are use GET method"
        }
        return Response(response_data, status.HTTP_400_BAD_REQUEST, content_type="application/json")


@api_view(['GET'])
@permission_classes([AllowAny, ])
def get_one_product(request, id):
    try:
        one_product = Products_shop.objects.get(id_support_product=id)
    except Exception as e:
        response_data = {
            "status": "Failed",
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"There is something wrong: {str(e)}"
        }
        return Response(response_data, status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="application/json")
    if request.method == "GET":
        serializer = ProductSerializer(one_product)
        response_data = {
            "status": "ok",
            "code": status.HTTP_200_OK,
            "total": len(serializer.data),
            "data": serializer.data
        }
        return Response(response_data, status.HTTP_200_OK, content_type="application/json")
    else:
        response_data = {
            "status": "Failed",
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Be Sure You are use GET method"
        }
        return Response(response_data, status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="application/json")


#################################### END Section of Products ###############################################################

#################################### Start Section of Cart Items ###############################################################

@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
@authentication_classes([JWTAuthentication])
def get_items_of_card(request):
    user = request.user
    if request.method == "GET":
        get_all_items = CartItem.objects.filter(user=user)
        serializer = CartItemSerializer(get_all_items, many=True)

        totally = sum(item.quantity * item.price for item in get_all_items)
        response_data = {
            "status": "ok",
            "code": status.HTTP_200_OK,
            "totally": totally,
            "data": serializer.data
        }
        return Response(response_data, status.HTTP_200_OK, content_type="application/json")


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
@authentication_classes([JWTAuthentication])
@cart_item_validate
def add_items_to_card(request):
    if request.method == "POST":
        serializer = CartItemSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    "status": "ok",
                    "code": status.HTTP_201_CREATED,
                    "total": len(serializer.data),
                    "message": "Item Created Successfully",
                    "data": serializer.data
                }
                return Response(response_data, status.HTTP_201_CREATED, content_type="application/json")
            else:
                response_data = {
                    "status": "Failed",
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "There is something wrong with your form"
                }
                return Response(response_data, status.HTTP_400_BAD_REQUEST, content_type="application/json")
        except Exception as e:
            response_data = {
                "status": "Failed",
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": f"There is something wrong: {str(e)}"
            }
            return Response(response_data, status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="application/json")
    else:
        response_data = {
            "status": "Failed",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Be sure You are using POST Method"
        }
        return Response(response_data, status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="application/json")


@api_view(['PUT'])
@permission_classes([IsAuthenticated, ])
@authentication_classes([JWTAuthentication])
def edit_items_card(request, id):
    try:
        id_card_item = CartItem.objects.get(id=id)
    except Exception as e:
        response_data = {
            "status": "Failed",
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"There is something wrong: {str(e)}"
        }
        return Response(response_data, status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="application/json")

    if request.method == "PUT":
        serializer = CartItemSerializer(id_card_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "status": "ok",
                "code": status.HTTP_200_OK,
                "total": len(serializer.data),
                "message": "Item updated successfully",
                "data": serializer.data
            }
            return Response(response_data, status.HTTP_200_OK, content_type="application/json")
        else:
            response_data = {
                "status": "Failed",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "There is something wrong with your form"
            }
            return Response(response_data, status.HTTP_400_BAD_REQUEST, content_type="application/json")


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, ])
@authentication_classes([JWTAuthentication])
def delete_item_card(request, id):
    try:
        id_card_item = CartItem.objects.get(id=id)
    except Exception as e:
        response_data = {
            "status": "Failed",
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"There is something wrong: {str(e)}"
        }
        return Response(response_data, status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="application/json")

    if request.method == "DELETE":
        id_card_item.delete()
        response_data = {
            "status": "ok",
            "code": status.HTTP_200_OK,
            "message": "Item deleted successfully",
        }
        return Response(response_data, status.HTTP_200_OK, content_type="application/json")


#################################### END Section of Cart Items ###############################################################


#################################### Start Section of Order ###############################################################

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, ])
def add_order(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)

    try:
        if request.method == "POST":
            last_record = Order.objects.order_by('-customer_id_order').first()

            if last_record is None:
                last_value = 1001
            else:
                last_value = last_record.customer_id_order + 1

            new_id_customer = last_value

            with transaction.atomic():
                for cart_add in cart_items:
                    Order.objects.create(
                        customer_id_order=new_id_customer,
                        user=user,
                        product_name=cart_add.product_name,
                        color=cart_add.color,
                        size=cart_add.size,
                        price=cart_add.price,
                        quantity=cart_add.quantity,
                        status="Unpaid",
                    )
                    delete_item = CartItem.objects.get(pk=cart_add.pk)
                    delete_item.delete()

            response_data = {
                "status": "ok",
                "code": status.HTTP_201_CREATED,
                "message": "Order Created Successfully",
            }
            return Response(response_data, status.HTTP_201_CREATED)
    except Exception as e:
        response_data = {
            "status": "Failed",
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"There is something wrong: {str(e)}"
        }
        return Response(response_data, status.HTTP_500_INTERNAL_SERVER_ERROR)

# def add_order(request):
#     user = request.user
#     cart_item = CartItem.objects.filter(user=user)
#     try:
#         if request.method == "POST":
#             last_record = Order.objects.order_by('-customer_id_order').first()
#
#             if last_record is None:
#                 last_value = 1001
#             else:
#                 last_value = last_record.customer_id_order + 1
#
#             new_id_customer = last_value
#             # try:
#             #
#             # except Exception as e:
#             #     response_data = {
#             #                     "status": "Failed",
#             #                     "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
#             #                     "message": f"There is something wrong: {str(e)}"
#             #                 }
#             #     return Response(response_data, status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="application/json")
#             with transaction.atomic():
#                 for card_add in cart_item:
#                     cart_serializer = CartItemSerializer(data=card_add)
#                     if cart_serializer.is_valid():
#                         order_data = {
#                             'customer_id_order': new_id_customer,
#                             'user': user,
#                             'product_name': cart_serializer.validated_data['product_name'],
#                             'color': cart_serializer.validated_data['color'],
#                             'size': cart_serializer.validated_data['size'],
#                             'price': cart_serializer.validated_data['price'],
#                             'quantity': cart_serializer.validated_data['quantity'],
#                             'status': 'Unpaid',
#                         }
#                         Order.objects.create(**order_data)
#                         card_add.delete()
#             response_data = {
#                 "status": "ok",
#                 "code": status.HTTP_201_CREATED,
#                 "message": "Order Created Successfully",
#             }
#             return Response(response_data, status.HTTP_201_CREATED, content_type="application/json")
#     except Exception as e:
#         response_data = {
#             "status": "Failed",
#             "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
#             "message": f"There is something wrong: {str(e)}"
#         }
#         return Response(response_data, status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="application/json")


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, ])
def get_all_order(request):
    try:
        user = request.user
        if request.method == "GET":
            get_all_orders = Order.objects.filter(user=user)
            serializer = OrderSerializer(get_all_orders, many=True)

            totally = sum(item.quantity * item.price for item in get_all_orders)
            response_data = {
                "status": "ok",
                "code": status.HTTP_200_OK,
                "totally": totally,
                "data": serializer.data
            }
            return Response(response_data, status.HTTP_200_OK, content_type="application/json")

    except Exception as e:
        response_data = {
            "status": "Failed",
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"There is something wrong: {str(e)}"
        }
        return Response(response_data, status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="application/json")
#################################### END Section of Order ###############################################################
