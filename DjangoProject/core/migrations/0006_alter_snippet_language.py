# Generated by Django 4.0.3 on 2022-03-25 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_snippet_linenos_remove_snippet_save_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippet',
            name='language',
            field=models.CharField(default='unknown', max_length=100),
        ),
    ]
