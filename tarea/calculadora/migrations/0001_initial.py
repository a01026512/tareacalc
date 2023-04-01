# Generated by Django 4.1.7 on 2023-03-30 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Jugadores",
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
                ("grupo", models.CharField(max_length=2)),
                ("num_lista", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Reto",
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
                ("nombre", models.CharField(max_length=30)),
                ("minutos_jugados", models.IntegerField()),
            ],
        ),
    ]