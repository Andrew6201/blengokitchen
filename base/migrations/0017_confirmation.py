# Generated by Django 4.2.4 on 2024-07-01 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_alter_contribution_confirmation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Confirmation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirmation', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]