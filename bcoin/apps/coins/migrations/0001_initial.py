# Generated by Django 4.0 on 2021-12-17 00:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TransactionId",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("current_value", models.PositiveBigIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="Wallet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_id", models.CharField(db_index=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="CoinTransfer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("transaction_id", models.IntegerField(db_index=True)),
                ("amount", models.DecimalField(decimal_places=3, max_digits=12)),
                ("date", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "wallet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="coins.wallet"
                    ),
                ),
            ],
        ),
    ]
