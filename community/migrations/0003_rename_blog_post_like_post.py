# Generated by Django 5.0.4 on 2024-05-06 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_rename_blog_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='blog_post',
            new_name='post',
        ),
    ]
