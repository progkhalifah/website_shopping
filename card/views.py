import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.urls import reverse

from product.models import *

import os

# os.add_dll_directory(r"C:\Program Files\GTK3-Runtime Win64\bin")

os.environ['TMP'] = 'C:/Users/EngKhalifah/AppData/Local/Temp/rb'

from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile


@login_required
def cart(request):
    user = request.user
    card = CartItem.objects.filter(user=user)
    totally = sum(item.quantity * item.price for item in card)
    context = {
        "items": card,
        "totally": totally,
    }
    return render(request, "pages/cart.html", context)


def cart_items_count(request):
    user = request.user
    if user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        cart_count = cart_items.count()
    else:
        cart_count = 0
    return {"cart_items_count": cart_count}


def delete_item_card(request, pk):
    if request.method == "GET":
        CartItem.objects.filter(pk=pk).delete()
    return redirect("card:cart")


def edit_item_card(request):
    if request.method == "POST":
        if "btn_update" in request.POST:
            cart_id = request.POST.get("id_item")
            edtxt_item = request.POST.get("edtxt_quantity")
            print("This is the updated quantity:", edtxt_item)
            CartItem.objects.filter(pk=cart_id).update(quantity=edtxt_item)
            return redirect("card:cart")
    return redirect("card:cart")


def add_order(request):
    user = request.user
    cart_item = CartItem.objects.filter(user=user)
    if request.method == "POST":
        if "btn_add_order" in request.POST:
            last_record = Order.objects.order_by('-customer_id_order').first()

            if last_record is None:
                last_value = 1001
            else:
                last_value = last_record.customer_id_order + 1

            new_id_customer = last_value

            with transaction.atomic():
                for cart_add in cart_item:
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
            messages.success(request, "Your order created successfully")
            return redirect("card:checkout")
    return redirect("card:cart")


def check_out(request):
    user = request.user
    order_items = Order.objects.filter(user=user, status="Unpaid")
    order_total = sum(order_item.quantity * order_item.price for order_item in order_items)

    if order_items.exists():
        specifice_order = order_items.first()

        order_customer_id = specifice_order.customer_id_order
        request.session['invoice_id'] = order_customer_id
    else:
        order_customer_id = None

    if request.method == "POST" and "btn_paid" in request.POST:
        with transaction.atomic():
            for order_item in order_items:
                try:
                    order_of_id = Order.objects.get(order_id=order_item.order_id)
                    item_total = order_item.quantity * order_item.price
                    invoice = Invoice.objects.create(
                        user=user,
                        invoice_number=order_item.customer_id_order,
                        total_amount=item_total,
                    )
                    invoice.order.add(order_of_id)
                    order_item.status = "Pending"
                    order_item.save()
                except Order.DoesNotExist:
                    # Handle the case when no matching order is found
                    print("Order not found", )

            # Redirect to the "successful" page
            return redirect("card:successfully")

    context = {
        "order_items": order_items,
        "order_total": order_total,
        "order_customer_id": order_customer_id,
    }
    return render(request, "pages/checkout.html", context)


def successfully(request):
    return render(request, "pages/thankyou.html")


def export_pdf(request):
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = "inline; attachment; filename=Invoices.pdf" + str(
        datetime.datetime.now()) + '.pdf'
    response["Content-Transfer-Encoding"] = "binary"
    get_invoice_id = request.session.get('invoice_id')
    if get_invoice_id is None:
        print("there is something wrong")
    else:
        print("This is the Id of invoice:", get_invoice_id)

    invoice = Invoice.objects.filter(user=request.user, invoice_number=get_invoice_id)
    invoice_total = sum(invoice_item.total_amount for invoice_item in invoice)

    html_string = render_to_string('reports/invoice_pdf.html', {'invoice': invoice, 'total': invoice_total})
    html = HTML(string=html_string)

    # Specify a custom temporary directory
    custom_temp_dir = 'C:/Users/EngKhalifah/Desktop/invoices'
    os.makedirs(custom_temp_dir, exist_ok=True)  # Create the directory if it doesn't exist
    tempfile.tempdir = custom_temp_dir

    # Generate the PDF
    result = html.write_pdf()

    # Write the PDF to the response
    response.write(result)

    return response

# def export_pdf(request):
#
#     response = HttpResponse(content_type="application/pdf")
#     response['Content-Disposition'] = "inline; attachment; filename=Invoices" + str(datetime.datetime.now())+'.pdf'
#     response["Content-Transfer-Encoding"] = "binary"
#
#     invoice = Invoice.objects.filter(user=request.user)
#
#     # sum = invoice.aggregates(Sum('total_amount'))
#
#     html_string = render_to_string(
#         'reports/invoice_pdf.html', {'invoices': [], 'total': 0}
#     )
#     html = HTML(string=html_string)
#     result = html.write_pdf()
#
#     with tempfile.NamedTemporaryFile(delete=True) as output:
#         output.write(result)
#         output.flush()
#         output = open(output.name, 'rb')
#         response.write(output.read())
#
#     # html = HTML(string=html_string)
#     # pdf_file = tempfile.NamedTemporaryFile(delete=False)
#     # html.write_pdf(target=pdf_file)
#
#     return response
