# Generated by Django 2.2.5 on 2020-02-09 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0002_auto_20200209_0149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='carb_target',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='fat_target',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='protein_target',
            field=models.IntegerField(default=0),
        ),
    ]
