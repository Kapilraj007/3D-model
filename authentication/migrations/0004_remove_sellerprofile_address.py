# Generated by Django 5.0.4 on 2024-04-28 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_address_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sellerprofile',
            name='address',
        ),
    ]