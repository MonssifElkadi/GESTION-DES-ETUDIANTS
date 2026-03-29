from django.db import models
from subject.models import Subject
from student.models import Student

class Exam(models.Model):
    name          = models.CharField(max_length=100)
    subject       = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date          = models.DateField()
    start_time    = models.TimeField()
    student_class = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} - {self.subject}"


class ExamResult(models.Model):
    exam           = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student        = models.ForeignKey(Student, on_delete=models.CASCADE)
    marks          = models.FloatField()
    grade          = models.CharField(max_length=5, blank=True)

    class Meta:
        unique_together = ('exam', 'student')

    def save(self, *args, **kwargs):
        # Auto-calculate grade from marks
        if self.marks >= 10:
            self.grade = 'V'
        elif self.marks >= 7 and self.marks < 10:
            self.grade = 'RATT'
        else:
            self.grade = 'NV'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.exam}: {self.marks}"