# Generated by Django 4.0.3 on 2022-03-20 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_snippet_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippet',
            name='owner',
            field=models.CharField(max_length=100),
        ),
    ]
