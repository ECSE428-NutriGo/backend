# Generated by Django 2.2.5 on 2020-02-06 01:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('nutrition', '0003_meal_mealentry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mealentry',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
