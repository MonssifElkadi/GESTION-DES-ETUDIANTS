import json
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect
from django.utils import timezone
from student.models import Student
from teacher.models import Teacher
from departement.models import Department
from subject.models import Subject
from exam.models import ExamResult
from timetable.models import TimeTable
from holiday.models import Holiday

DAY_LABELS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']


def build_day_chart_data(day_totals):
    counts = {day: 0 for day in DAY_LABELS}
    for item in day_totals:
        day = item.get('day')
        if day in counts:
            counts[day] = item.get('total', 0)
    return {
        'labels': DAY_LABELS,
        'counts': [counts[day] for day in DAY_LABELS],
    }

@login_required(login_url='login')
def index(request):
    if request.user.is_admin or request.user.is_superuser:
        class_totals = (
            Student.objects.values('student_class')
            .annotate(total=Count('id'))
            .order_by('student_class')
        )
        class_labels = []
        class_counts = []
        for item in class_totals:
            label = item.get('student_class') or 'Unassigned'
            class_labels.append(label)
            class_counts.append(item.get('total', 0))
        context = {
            'student_count': Student.objects.count(),
            'teacher_count': Teacher.objects.count(),
            'department_count': Department.objects.count(),
            'subject_count': Subject.objects.count(),
            'student_class_chart': json.dumps({
                'labels': class_labels,
                'counts': class_counts,
            }),
        }
        return render(request, 'Home/admin_dashboard.html', context)
    
    elif request.user.is_teacher:
        today = timezone.localdate()
        end_date = today + timedelta(days=30)
        upcoming_holidays = Holiday.objects.filter(
            date__range=(today, end_date)
        ).order_by('date')
        teacher_profile = (
            Teacher.objects.filter(email=request.user.email).first()
            or Teacher.objects.filter(
                first_name=request.user.first_name,
                last_name=request.user.last_name,
            ).first()
        )
        if teacher_profile:
            teacher_day_totals = (
                TimeTable.objects.filter(teacher=teacher_profile)
                .values('day')
                .annotate(total=Count('id'))
            )
        else:
            teacher_day_totals = []
        teacher_class_load_chart = build_day_chart_data(teacher_day_totals)
        context = {
            'teacher_profile': teacher_profile,
            'upcoming_holidays': upcoming_holidays,
            'subjects': Subject.objects.all()[:5],
            'timetables': TimeTable.objects.all()[:5],
            'teacher_class_load_chart': json.dumps(teacher_class_load_chart),
        }
        return render(request, 'Home/teacher_dashboard.html', context)
        
    else:
        today = timezone.localdate()
        end_date = today + timedelta(days=30)
        upcoming_holidays = Holiday.objects.filter(
            date__range=(today, end_date)
        ).order_by('date')
        student = (
            Student.objects.filter(parent__father_email=request.user.email).first()
            or Student.objects.filter(parent__mother_email=request.user.email).first()
            or Student.objects.filter(
                first_name=request.user.first_name,
                last_name=request.user.last_name,
            ).first()
        )
        if student and student.student_class:
            timetables = TimeTable.objects.filter(
                student_class=student.student_class
            ).order_by('day', 'start_time')[:5]
            student_day_totals = (
                TimeTable.objects.filter(student_class=student.student_class)
                .values('day')
                .annotate(total=Count('id'))
            )
        else:
            timetables = TimeTable.objects.none()
            student_day_totals = []

        student_class_load_chart = build_day_chart_data(student_day_totals)

        # Default to student dashboard
        context = {
            'results': ExamResult.objects.all()[:5],
            'student_profile': student,
            'upcoming_holidays': upcoming_holidays,
            'timetables': timetables,
            'student_class_load_chart': json.dumps(student_class_load_chart),
        }
        return render(request, 'Home/student_dashboard.html', context)

@login_required(login_url='login')
def dashboard(request):
    return redirect('index')