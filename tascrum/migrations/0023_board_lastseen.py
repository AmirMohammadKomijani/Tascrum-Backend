# Generated by Django 4.2.6 on 2023-11-11 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tascrum', '0022_alter_board_backgroundimage_alter_card_reminder_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='lastseen',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
