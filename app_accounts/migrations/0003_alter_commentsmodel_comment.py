# Generated by Django 4.0.2 on 2022-02-15 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_accounts', '0002_commentsmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentsmodel',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
