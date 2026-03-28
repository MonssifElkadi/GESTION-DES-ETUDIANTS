import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from departement.models import Department
from teacher.models import Teacher
from subject.models import Subject
from timetable.models import TimeTable
from datetime import time

# 1. Create a Department
dept, _ = Department.objects.get_or_create(
    name="Computer Science",
    defaults={'description': "IT and Programming Department"}
)

# 2. Create a Teacher
teacher, _ = Teacher.objects.get_or_create(
    teacher_id="T-1001",
    defaults={
        'first_name': "Alan",
        'last_name': "Turing",
        'gender': "Male",
        'date_of_birth': "1980-01-01",
        'email': "alan.turing@preskool.com",
        'mobile_number': "0606060606",
        'department': dept,
        'joining_date': "2026-01-01"
    }
)

# 3. Create a Subject
subject, _ = Subject.objects.get_or_create(
    subject_code="CS101",
    defaults={
        'name': "Introduction to Python",
        'department': dept,
        'teacher': teacher
    }
)

# 4. Create some TimeTable Entries
TimeTable.objects.get_or_create(
    day="Monday",
    start_time=time(8, 0),
    end_time=time(10, 0),
    subject=subject,
    student_class="Grade 10A",
    defaults={'teacher': teacher}
)

TimeTable.objects.get_or_create(
    day="Wednesday",
    start_time=time(10, 30),
    end_time=time(12, 30),
    subject=subject,
    student_class="Grade 10A",
    defaults={'teacher': teacher}
)

print("✅ Data successfully seeded: 1 Department, 1 Teacher, 1 Subject, 2 Timetable entries!")
