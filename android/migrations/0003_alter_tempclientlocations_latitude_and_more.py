# Generated by Django 5.0 on 2024-01-04 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('android', '0002_uniquekey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tempclientlocations',
            name='latitude',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='tempclientlocations',
            name='longitude',
            field=models.FloatField(),
        ),
    ]
