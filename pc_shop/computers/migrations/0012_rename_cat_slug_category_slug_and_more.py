# Generated by Django 4.1.7 on 2023-03-17 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('computers', '0011_remove_category_details'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='cat_slug',
            new_name='slug',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='product_slug',
            new_name='slug',
        ),
    ]
