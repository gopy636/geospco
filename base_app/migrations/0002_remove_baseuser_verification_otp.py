# Generated by Django 4.0.2 on 2022-02-13 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='baseuser',
            name='verification_otp',
        ),
    ]
