from django.db import models
from departement.models import Department

class Teacher(models.Model):
    first_name    = models.CharField(max_length=100)
    last_name     = models.CharField(max_length=100)
    teacher_id    = models.CharField(max_length=20, unique=True)
    gender        = models.CharField(max_length=10, choices=[('Male','Male'),('Female','Female')])
    date_of_birth = models.DateField()
    email         = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15)
    address       = models.TextField(blank=True)
    department    = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    teacher_image = models.ImageField(upload_to='teachers/', blank=True)
    joining_date  = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
