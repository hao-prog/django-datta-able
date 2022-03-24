# Generated by Django 3.2.11 on 2022-03-23 04:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0001_initial'),
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseTeacher',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('deleted', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.course')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.teacher')),
            ],
            options={
                'db_table': 'course_teacher',
            },
        ),
    ]
