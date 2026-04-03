from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100 , unique=True)
    description = models.TextField(blank=True)
    head_teacher = models.ForeignKey('teacher.Teacher', on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_departments')

    def __str__(self):
        return self.name
