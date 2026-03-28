from django.db import models
from subject.models import Subject
from teacher.models import Teacher

DAYS = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
]

class TimeTable(models.Model):
    day           = models.CharField(max_length=10, choices=DAYS)
    start_time    = models.TimeField()
    end_time      = models.TimeField()
    subject       = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher       = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    student_class = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.day} - {self.subject} ({self.student_class})"