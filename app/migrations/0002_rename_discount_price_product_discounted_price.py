# Generated by Django 4.0 on 2022-12-28 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='discount_price',
            new_name='discounted_price',
        ),
    ]
