# Generated by Django 3.1.4 on 2021-02-05 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20210205_1020'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recieve',
            old_name='summa',
            new_name='dollar',
        ),
        migrations.AddField(
            model_name='recieve',
            name='som',
            field=models.FloatField(default=0),
        ),
    ]
