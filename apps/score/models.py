import uuid
from django.db import models
from django.db.models import Q
from apps.student.models import Student
from apps.course.models import Course
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator


class Score(models.Model):
    class Meta:
        db_table = "score"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(0)]
    )
    description = models.TextField(max_length=1000, blank=True, null=True)
    deleted = models.BooleanField(default=False)

    def get_by_id(id):
        score = Score.objects.get(pk=id, deleted=False)
        return score

    def get_scores_by(keyword=None, student_name=None, course_name=None):
        condition = Q(deleted=False)
        if keyword:
            condition &= Q(description__icontains=keyword)
        if student_name:
            condition &= Q(student__name__icontains=student_name)
        if course_name:
            condition &= Q(course__name__icontains=course_name)

        return Score.objects.filter(condition)

    def create(student_id, course_id, score, description):
        if not student_id:
            raise ValidationError({"student_id": ["This field cannot be blank."]})
        if not course_id:
            raise ValidationError({"course_id": ["This field cannot be blank."]})
        if Score.objects.filter(student_id=student_id, course_id=course_id).exists():
            raise ValidationError({"score": "Score is existed"})
        score = Score(
            student_id=student_id,
            course_id=course_id,
            score=score,
            description=description,
        )
        score.clean_fields()
        score.save()

    def update(self, student_id, course_id, score, description):
        if not student_id:
            raise ValidationError({"student_id": ["This field cannot be blank."]})
        if not course_id:
            raise ValidationError({"course_id": ["This field cannot be blank."]})
        if (
            Score.objects.filter(student_id=student_id, course_id=course_id)
            .exclude(id=self.id)
            .exists()
        ):
            raise ValidationError({"score": "Score is existed"})
        self.student_id = student_id
        self.course_id = course_id
        self.score = score
        self.description = description
        self.clean_fields()
        self.save()

    def delete(self):
        self.deleted = True
        self.save()
