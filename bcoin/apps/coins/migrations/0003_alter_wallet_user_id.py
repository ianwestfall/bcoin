# Generated by Django 4.0 on 2021-12-17 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0002_auto_20211217_0049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='user_id',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
