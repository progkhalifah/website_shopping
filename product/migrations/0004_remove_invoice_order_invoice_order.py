# Generated by Django 4.2.4 on 2023-10-29 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_edit_order_and_create_invoice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='order',
        ),
        migrations.AddField(
            model_name='invoice',
            name='order',
            field=models.ManyToManyField(to='product.order'),
        ),
    ]
