# Generated by Django 4.0.3 on 2022-03-20 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='snippet',
            name='highlighted',
        ),
        migrations.AlterField(
            model_name='snippet',
            name='owner',
            field=models.CharField(default=None, max_length=20),
        ),
    ]
