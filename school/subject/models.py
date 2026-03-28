from django.db import models
from departement.models import Department
from teacher.models import Teacher

class Subject(models.Model):
    name         = models.CharField(max_length=100)
    subject_code = models.CharField(max_length=20, unique=True)
    department   = models.ForeignKey(Department, on_delete=models.CASCADE)
    teacher      = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.subject_code} - {self.name}"