# Generated by Django 4.2.6 on 2023-11-08 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tascrum', '0019_card_setestimate_card_storypoint'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checklist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60, null=True)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Icard', to='tascrum.card')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255, null=True)),
                ('checked', models.BooleanField(default=False)),
                ('checklist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ichecklist', to='tascrum.checklist')),
            ],
        ),
    ]