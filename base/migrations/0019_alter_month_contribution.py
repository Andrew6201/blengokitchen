# Generated by Django 4.2.4 on 2024-07-01 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_delete_confirmation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='month',
            name='contribution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.contribution'),
        ),
    ]
