# Generated by Django 4.1.7 on 2023-03-06 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('computers', '0004_category_photo_category_plural_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='company',
            field=models.CharField(default='NVIDIA', max_length=20),
            preserve_default=False,
        ),
    ]
