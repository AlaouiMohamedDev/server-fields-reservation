# Generated by Django 4.1.7 on 2023-04-27 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_user_is_staff_remove_user_is_superuser_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_pic',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
