# Generated by Django 3.2.5 on 2022-01-09 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='discount_approved',
            field=models.BooleanField(default=False),
        ),
    ]
