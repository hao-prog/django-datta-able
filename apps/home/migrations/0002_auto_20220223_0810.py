# Generated by Django 3.2.11 on 2022-02-23 08:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='birthday_year',
            new_name='user_name',
        ),
        migrations.RemoveField(
            model_name='student',
            name='date',
        ),
    ]