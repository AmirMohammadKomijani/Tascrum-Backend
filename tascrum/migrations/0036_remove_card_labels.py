# Generated by Django 4.2.6 on 2023-11-20 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tascrum', '0035_merge_20231120_1450'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='labels',
        ),
    ]
