# Generated by Django 3.2 on 2022-11-29 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0005_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='mobile_number',
            field=models.IntegerField(),
        ),
    ]
