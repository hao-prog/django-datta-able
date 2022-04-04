import uuid
from django.db import models
from django.db.models import Q
from apps.subject.models import Subject
from django.core.exceptions import ValidationError
from apps.teacher.models import Teacher
from apps.student.models import Student


class Course(models.Model):
    class Meta:
        db_table = "course"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000, blank=True, null=True)
    deleted = models.BooleanField(default=False)

    def get_by_id(id):
        course = Course.objects.get(pk=id, deleted=False)
        return course

    def get_courses_by(keyword=None):
        condition = Q(deleted=False)
        if keyword:
            keyword_condition = Q(name__icontains=keyword) | Q(
                description__icontains=keyword
            )
            condition &= keyword_condition

        return Course.objects.filter(condition)

    def create(name, subject_id, description):
        if Course.objects.filter(name=name, deleted=False).exists():
            raise ValidationError({"name": "Name of course is existed"})
        course = Course(
            name=name,
            subject_id=subject_id,
            description=description,
        )
        course.clean_fields()
        course.save()
        return course

    def update(self, name, subject, description):
        if Course.objects.filter(name=name, deleted=False).exclude(id=self.id).exists():
            raise ValidationError({"name": "Name of course is existed"})
        self.name = name
        self.subject = subject
        self.description = description
        self.clean_fields()
        self.save()

    def delete(self):
        self.deleted = True
        self.save()

    def get_teacher_list(self):
        id_array = self.courseteacher_set.filter(deleted=False).values_list(
            "teacher_id"
        )
        return Teacher.objects.filter(id__in=id_array)

    def get_teachers_exclude(self):
        id_array = self.courseteacher_set.filter(deleted=False).values_list(
            "teacher_id"
        )
        result = Teacher.objects.filter(deleted=False).exclude(id__in=id_array)
        return result

    def get_student_list(self):
        id_array = self.coursestudent_set.filter(deleted=False).values_list(
            "student_id"
        )
        return Student.objects.filter(id__in=id_array)

    def get_students_exclude(self):
        id_array = self.coursestudent_set.filter(deleted=False).values_list(
            "student_id"
        )
        result = Student.objects.filter(deleted=False).exclude(id__in=id_array)
        return result


class CourseTeacher(models.Model):
    class Meta:
        db_table = "course_teacher"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)

    def get_by(course_id=None, teacher_id=None):
        course_teacher = CourseTeacher.objects.get(
            course_id=course_id, teacher_id=teacher_id, deleted=False
        )
        return course_teacher

    def create(course_id, teacher_id):
        if not teacher_id:
            raise ValidationError({"teacher": ["This field cannot be blank."]})
        course_teacher = CourseTeacher(course_id=course_id, teacher_id=teacher_id)
        course_teacher.clean_fields()
        course_teacher.save()

    def delete(self):
        self.deleted = True
        self.save()


class CourseStudent(models.Model):
    class Meta:
        db_table = "course_student"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)

    def get_by(course_id=None, student_id=None):
        course_student = CourseStudent.objects.get(
            course_id=course_id, student_id=student_id, deleted=False
        )
        return course_student

    def create(course_id, student_id):
        if not student_id:
            raise ValidationError({"student": ["This field cannot be blank."]})
        course_student = CourseStudent(course_id=course_id, student_id=student_id)
        course_student.clean_fields()
        course_student.save()

    def delete(self):
        self.deleted = True
        self.save()
