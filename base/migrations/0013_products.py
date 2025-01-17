# Generated by Django 5.0.6 on 2024-06-25 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_alter_chat_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productimage', models.ImageField(upload_to='product_images')),
                ('productname', models.CharField(max_length=1000000)),
                ('productprice', models.CharField(max_length=1000000)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
