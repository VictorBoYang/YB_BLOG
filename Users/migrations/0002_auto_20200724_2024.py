# Generated by Django 2.2.6 on 2020-07-24 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, upload_to='photo/%Y%m%d/'),
        ),
    ]
