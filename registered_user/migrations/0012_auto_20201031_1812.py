# Generated by Django 3.1.1 on 2020-10-31 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registered_user', '0011_auto_20201030_0011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_details',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
