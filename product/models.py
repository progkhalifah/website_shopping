import random
import uuid

from django.db import models
from django.contrib.auth.models import User

from authentication.models import CustomUser
from django9onlinestore_edit import settings


# Create your models here.

class Color_product(models.Model):
    # id_support_color = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name_color = models.TextField(default="none", max_length=250, help_text="Enter Name of the Color", null=False)

    def __str__(self):
        return self.name_color

    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colors'


class Size_product(models.Model):
    # id_support_size = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name_size = models.TextField(default="none", max_length=250, help_text="Enter the Size", null=False)

    def __str__(self):
        return self.name_size

    class Meta:
        verbose_name = 'Size'
        verbose_name_plural = 'Sizes'


class Products_shop(models.Model):
    id_support_product = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name_product = models.CharField(max_length=250, help_text="Enter Name of Product",
                                    error_messages="you have to enter name of product",
                                    )
    describe_product = models.TextField(blank=True, help_text="Enter Your describe product")
    image_product = models.FileField(upload_to="project_images/", blank=True)
    price_product = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=False,
                                        help_text="Enter the Price of Product",
                                        error_messages="You have to enter price of product")
    colors = models.ManyToManyField(Color_product)
    sizes = models.ManyToManyField(Size_product)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_product

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Add fields for order-specific details (e.g., shipping address)
    def __str__(self):
        return self.user

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_name = models.TextField(default=" ", max_length=250, help_text="Enter Name of the Color", null=False)
    color = models.TextField(default="none", max_length=250, help_text="Enter Name of the Color", null=True)
    size = models.TextField(default="none", max_length=250, help_text="Enter the Size", null=True)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=False,
                                help_text="Enter the Price of Product",
                                error_messages="You have to enter price of product")
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{CustomUser.username} {self.product_name}"

    def total_price(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = 'CartItem'
        verbose_name_plural = 'CartItems'


STATUS_CHOICES = [
    ('Unpaid', 'Unpaid'),
    ('Pending', 'Pending'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
]


class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    customer_id_order = models.PositiveBigIntegerField(default=1001, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_name = models.TextField(default=" ", max_length=250, help_text="Enter Name of the Color", null=False)
    color = models.TextField(default="none", max_length=250, help_text="Enter Name of the Color", null=True)
    size = models.TextField(default="none", max_length=250, help_text="Enter the Size", null=False)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=False,
                                help_text="Enter the Price of Product",
                                error_messages="You have to enter price of product")
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Unpaid')

    def __str__(self):
        return f"{CustomUser.username} {self.customer_id_order}"

    def total_price_order(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products_shop, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    # Add fields for tracking order item status and shipment details
    def __str__(self):
        return self.order

    class Meta:
        verbose_name = 'OrderItem'
        verbose_name_plural = 'OrderItems'


class Invoice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, default=settings.AUTH_USER_MODEL)
    order = models.ManyToManyField(Order,)
    invoice_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Invoice #{self.invoice_number}"


    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'



# from django.db import models
# from django.contrib.auth.models import User
#
# class Category(models.Model):
#     name = models.CharField(max_length=100)
#     slug = models.SlugField(unique=True)
#     # Add other fields as needed (e.g., description)
#
# class Product(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     stock = models.PositiveIntegerField()
#     # Add fields for product variations (e.g., size, color)
#     # Add fields for images, specifications, and other details
#
# class ProductReview(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     rating = models.PositiveIntegerField()
#     comment = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#
# class Cart(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # Add fields for order-specific details (e.g., shipping address)
#
# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#
# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     status = models.CharField(max_length=20)
#     # Add fields for order-specific details (e.g., order date, payment details)
#
# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     # Add fields for tracking order item status and shipment details


# class Payment(models.Model):
#     order = models.OneToOneField(Order, on_delete=models.CASCADE)
#     method = models.CharField(max_length=50)
#     card_number = models.CharField(max_length=16)
#     # Add other payment-related fields
#
# class Discount(models.Model):
#     code = models.CharField(max_length=20)
#     percentage = models.DecimalField(max_digits=5, decimal_places=2)
#     valid_from = models.DateTimeField()
#     valid_until = models.DateTimeField()
#     # Add fields for usage limits, restrictions, etc.
#
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     address = models.TextField()
#     phone = models.CharField(max_length=15)
#     # Add more fields for user profile information
#
# class ReturnRequest(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     reason = models.TextField()
#     refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=20)
#     # Add fields for return shipping and tracking details
#
# # Email notifications can be handled through Django's built-in email functionality or via a third-party package.
