# Generated by Django 4.2.2 on 2023-06-16 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ooredoo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_OO', models.IntegerField(null=True)),
                ('out_OO', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Orange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_OR', models.IntegerField(null=True)),
                ('out_OR', models.IntegerField(null=True)),
            ],
        ),
    ]
