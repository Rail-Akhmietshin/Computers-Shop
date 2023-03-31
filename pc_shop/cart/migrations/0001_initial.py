# Generated by Django 4.1.7 on 2023-03-27 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(verbose_name='creation date')),
                ('checked_out', models.BooleanField(default=False, verbose_name='checked out')),
            ],
            options={
                'verbose_name': ('cart',),
                'verbose_name_plural': ('carts',),
                'ordering': ('-creation_date',),
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='quantity')),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=18, verbose_name='unit price')),
                ('object_id', models.PositiveIntegerField()),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.cart', verbose_name='cart')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': ('item',),
                'verbose_name_plural': ('items',),
                'ordering': ('cart',),
            },
        ),
    ]
