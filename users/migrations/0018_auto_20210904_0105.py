# Generated by Django 3.0.5 on 2021-09-04 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20210904_0052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='coverimage',
            field=models.ImageField(blank=True, null=True, upload_to='cover_pics'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='default.png', null=True, upload_to='profile_pics'),
        ),
    ]
