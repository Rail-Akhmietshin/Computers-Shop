# Generated by Django 4.1.7 on 2023-03-06 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('computers', '0006_specification_product_details'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='company',
        ),
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
        migrations.RemoveField(
            model_name='specification',
            name='frequency',
        ),
        migrations.AddField(
            model_name='specification',
            name='company',
            field=models.CharField(default=None, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='specification',
            name='description',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='specification',
            name='max_frequency',
            field=models.PositiveSmallIntegerField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='specification',
            name='min_frequency',
            field=models.PositiveSmallIntegerField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='specification',
            name='power',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='specification',
            name='generation',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='specification',
            name='latency',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
