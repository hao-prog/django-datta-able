# Generated by Django 3.2.11 on 2022-02-23 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20220223_0838'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='deleted',
            field=models.BooleanField(default=0),
        ),
    ]
