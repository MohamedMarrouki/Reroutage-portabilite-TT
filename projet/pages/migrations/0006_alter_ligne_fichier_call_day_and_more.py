# Generated by Django 4.2.2 on 2023-06-22 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_alter_ligne_fichier_call_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ligne_fichier',
            name='call_day',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='ligne_fichier',
            name='call_time',
            field=models.TimeField(null=True),
        ),
    ]
