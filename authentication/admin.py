from django.contrib import admin

from authentication.models import CustomUser


# Register your models here.
@admin.register(CustomUser)
class CustomUser(admin.ModelAdmin):
    list_display = ("first_name", "last_name")