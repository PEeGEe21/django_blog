# Generated by Django 3.0.5 on 2021-09-04 08:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20210904_0123'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='featured_image',
        ),
    ]
