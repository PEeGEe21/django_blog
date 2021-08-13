# Generated by Django 3.1.6 on 2021-08-12 18:54

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_profile_birthday'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='slug',
            field=autoslug.fields.AutoSlugField(default='', editable=False, populate_from='user'),
        ),
    ]
