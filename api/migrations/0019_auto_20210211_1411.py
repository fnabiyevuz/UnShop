# Generated by Django 3.1.4 on 2021-02-11 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_deliver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recieve',
            name='deliver',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.deliver'),
            preserve_default=False,
        ),
    ]
