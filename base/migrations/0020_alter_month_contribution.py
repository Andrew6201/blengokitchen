# Generated by Django 4.2.4 on 2024-07-01 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_alter_month_contribution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='month',
            name='contribution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.contribution'),
        ),
    ]