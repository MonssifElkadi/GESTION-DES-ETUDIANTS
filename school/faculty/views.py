from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from student.models import Student
from teacher.models import Teacher
from departement.models import Department
from subject.models import Subject
from exam.models import ExamResult
from timetable.models import TimeTable

@login_required(login_url='login')
def index(request):
    if request.user.is_admin or request.user.is_superuser:
        context = {
            'student_count': Student.objects.count(),
            'teacher_count': Teacher.objects.count(),
            'department_count': Department.objects.count(),
            'subject_count': Subject.objects.count(),
        }
        return render(request, 'Home/admin_dashboard.html', context)
    
    elif request.user.is_teacher:
        context = {
            'subjects': Subject.objects.all()[:5],
            'timetables': TimeTable.objects.all()[:5]
        }
        return render(request, 'Home/teacher_dashboard.html', context)
        
    else:
        # Default to student dashboard
        context = {
            'results': ExamResult.objects.all()[:5],
            'timetables': TimeTable.objects.all()[:5]
        }
        return render(request, 'Home/student_dashboard.html', context)

@login_required(login_url='login')
def dashboard(request):
    return redirect('index')