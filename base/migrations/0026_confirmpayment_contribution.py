# Generated by Django 5.0.6 on 2024-07-04 09:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0025_confirmpayment'),
    ]

    operations = [
        migrations.AddField(
            model_name='confirmpayment',
            name='contribution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.contribution'),
        ),
    ]