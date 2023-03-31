# Generated by Django 4.1.7 on 2023-03-06 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('computers', '0007_remove_product_company_remove_product_description_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='specification',
            old_name='max_frequency',
            new_name='frequency',
        ),
        migrations.RemoveField(
            model_name='specification',
            name='latency',
        ),
        migrations.RemoveField(
            model_name='specification',
            name='min_frequency',
        ),
    ]
