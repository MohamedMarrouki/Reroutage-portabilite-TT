# Generated by Django 4.2.2 on 2023-06-21 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuploadfile',
            name='date_upload',
            field=models.DateTimeField(),
        ),
    ]