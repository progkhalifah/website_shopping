# Generated by Django 4.2.4 on 2023-10-29 16:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0004_remove_invoice_order_invoice_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='user',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]