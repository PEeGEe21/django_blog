# Generated by Django 3.1.6 on 2021-08-10 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='name',
        ),
        migrations.AddField(
            model_name='profile',
            name='displayname',
            field=models.CharField(default=None, max_length=50, verbose_name='Display Name'),
        ),
    ]
