# Generated by Django 3.1.6 on 2021-08-12 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20210811_0016'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='birthday',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Birthday'),
        ),
    ]
