# Generated by Django 5.0.6 on 2024-06-23 16:01

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wardrobe_wizard', '0011_alter_lower_lower_alter_upper_upper'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lower',
            name='lower',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='upper',
            name='upper',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
    ]
