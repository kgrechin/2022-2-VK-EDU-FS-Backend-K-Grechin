# Generated by Django 4.1.3 on 2022-12-22 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='default/account.png', null=True, upload_to='user_avatars/'),
        ),
    ]
