# Generated by Django 5.0.6 on 2024-06-23 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wardrobe_wizard', '0014_alter_lower_lower_alter_upper_upper'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lower',
            name='lower',
            field=models.ImageField(upload_to='lowers/'),
        ),
        migrations.AlterField(
            model_name='upper',
            name='upper',
            field=models.ImageField(upload_to='uppers/'),
        ),
    ]
