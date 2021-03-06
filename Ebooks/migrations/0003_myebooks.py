# Generated by Django 3.1.5 on 2021-01-14 13:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Ebooks', '0002_auto_20210114_1216'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyEbooks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('ebook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Ebooks.ebook')),
            ],
            options={
                'unique_together': {('customer', 'ebook')},
            },
        ),
    ]
