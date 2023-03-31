# Generated by Django 4.1.7 on 2023-03-07 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('computers', '0009_rename_slug_product_product_slug_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='products',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='computers.category'),
            preserve_default=False,
        ),
    ]
