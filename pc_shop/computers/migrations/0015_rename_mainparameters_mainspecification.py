# Generated by Django 4.1.7 on 2023-03-19 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('computers', '0014_mainparameters'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MainParameters',
            new_name='MainSpecification',
        ),
    ]
