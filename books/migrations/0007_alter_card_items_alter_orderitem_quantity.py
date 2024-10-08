# Generated by Django 5.0.7 on 2024-08-26 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_order_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='items',
            field=models.ManyToManyField(blank=True, related_name='cards', to='books.carditem'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
    ]
