# Generated by Django 3.2.11 on 2022-03-31 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_student_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='avatar',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
