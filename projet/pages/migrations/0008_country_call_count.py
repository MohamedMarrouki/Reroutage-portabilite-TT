# Generated by Django 4.2.2 on 2023-07-04 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='call_count',
            field=models.IntegerField(null=True),
        ),
    ]
