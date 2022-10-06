# Generated by Django 3.1.4 on 2021-02-08 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_returnproduct_barcode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='debt',
            name='return_date',
        ),
        migrations.RemoveField(
            model_name='debt',
            name='shop',
        ),
        migrations.AddField(
            model_name='debt',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default='2021-02-08T00:00:00'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='debt',
            name='debt',
            field=models.FloatField(default=1000),
            preserve_default=False,
        ),
    ]
