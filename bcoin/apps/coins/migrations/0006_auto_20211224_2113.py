# Generated by Django 4.0 on 2021-12-24 21:13

from django.db import migrations


def forward(apps, schema_editor):
    TransactionId = apps.get_model("coins", "TransactionId")
    db_alias = schema_editor.connection.alias
    TransactionId.objects.using(db_alias).create()


def reverse(apps, schema_editor):
    TransactionId = apps.get_model("coins", "TransactionId")
    db_alias = schema_editor.connection.alias
    TransactionId.objects.using(db_alias).all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("coins", "0005_wallet_discord_id"),
    ]

    operations = [migrations.RunPython(forward, reverse)]