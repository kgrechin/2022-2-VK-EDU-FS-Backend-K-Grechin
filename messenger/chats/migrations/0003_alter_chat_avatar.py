# Generated by Django 4.1.3 on 2022-12-16 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='chat_avatars/'),
        ),
    ]