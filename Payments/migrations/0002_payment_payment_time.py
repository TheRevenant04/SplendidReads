# Generated by Django 3.1.5 on 2021-01-13 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]