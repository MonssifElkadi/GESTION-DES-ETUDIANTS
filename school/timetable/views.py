from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import TimeTable
from subject.models import Subject
from teacher.models import Teacher

def timetable_view(request):
    timetables = TimeTable.objects.all().order_by('day', 'start_time')
    return render(request, 'timetable/timetable.html', {'timetables': timetables})

def add_timetable(request):
    subjects = Subject.objects.all()
    teachers = Teacher.objects.all()
    if request.method == 'POST':
        day           = request.POST.get('day')
        start_time    = request.POST.get('start_time')
        end_time      = request.POST.get('end_time')
        student_class = request.POST.get('student_class')
        subject_id    = request.POST.get('subject')
        teacher_id    = request.POST.get('teacher')
        subject       = get_object_or_404(Subject, pk=subject_id)
        teacher       = Teacher.objects.filter(pk=teacher_id).first()
        TimeTable.objects.create(
            day=day,
            start_time=start_time,
            end_time=end_time,
            student_class=student_class,
            subject=subject,
            teacher=teacher,
        )
        messages.success(request, 'Timetable entry added successfully')
        return redirect('timetable_view')
    return render(request, 'timetable/add-timetable.html', {'subjects': subjects, 'teachers': teachers})

def edit_timetable(request, pk):
    entry    = get_object_or_404(TimeTable, pk=pk)
    subjects = Subject.objects.all()
    teachers = Teacher.objects.all()
    if request.method == 'POST':
        entry.day           = request.POST.get('day')
        entry.start_time    = request.POST.get('start_time')
        entry.end_time      = request.POST.get('end_time')
        entry.student_class = request.POST.get('student_class')
        subject_id          = request.POST.get('subject')
        teacher_id          = request.POST.get('teacher')
        entry.subject       = get_object_or_404(Subject, pk=subject_id)
        entry.teacher       = Teacher.objects.filter(pk=teacher_id).first()
        entry.save()
        messages.success(request, 'Timetable entry updated successfully')
        return redirect('timetable_view')
    return render(request, 'timetable/edit-timetable.html', {'entry': entry, 'subjects': subjects, 'teachers': teachers})

def delete_timetable(request, pk):
    entry = get_object_or_404(TimeTable, pk=pk)
    entry.delete()
    messages.success(request, 'Timetable entry deleted successfully')
    return redirect('timetable_view')