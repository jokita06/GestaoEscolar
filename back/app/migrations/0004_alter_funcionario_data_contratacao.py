# Generated by Django 5.2.1 on 2025-05-18 21:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_funcionario_data_contratacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='data_contratacao',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
