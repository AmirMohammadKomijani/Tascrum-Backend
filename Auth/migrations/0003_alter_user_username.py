# Generated by Django 4.2.6 on 2023-10-20 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Auth", "0002_remove_user_occupation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(default="user", max_length=20, null=True),
        ),
    ]