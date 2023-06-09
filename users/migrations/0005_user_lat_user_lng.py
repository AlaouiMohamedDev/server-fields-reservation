# Generated by Django 4.1.7 on 2023-05-10 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='lat',
            field=models.DecimalField(decimal_places=20, default=31.6144592, max_digits=22),
        ),
        migrations.AddField(
            model_name='user',
            name='lng',
            field=models.DecimalField(decimal_places=20, default=-7.9669165, max_digits=22),
        ),
    ]
