from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import TimeTable, DAYS
from subject.models import Subject
from teacher.models import Teacher
from student.models import Student
from home_auth.decorators import login_required_custom, teacher_required
from itertools import groupby

@login_required_custom
def timetable_view(request):
    # If student, only show their class's timetable
    if request.user.is_student and not request.user.is_admin and not request.user.is_teacher:
        # Try to find the student profile — by parent email, then by matching name
        student = (
            Student.objects.filter(parent__father_email=request.user.email).first()
            or Student.objects.filter(parent__mother_email=request.user.email).first()
            or Student.objects.filter(
                first_name=request.user.first_name,
                last_name=request.user.last_name
            ).first()
        )

        if student and student.student_class:
            # Student has a class — show their timetable
            timetables = list(TimeTable.objects.filter(
                student_class=student.student_class
            ).order_by('day', 'start_time'))
            timetable_by_class = {student.student_class: timetables}
        else:
            # No student profile found or class not assigned yet
            timetable_by_class = {}

        return render(request, 'timetable/timetable.html', {
            'timetable_by_class': timetable_by_class,
            'classes': list(timetable_by_class.keys()),
            'no_class': student is None or not student.student_class,
        })
    else:
        timetables = TimeTable.objects.all().order_by('student_class', 'day', 'start_time')
        timetable_by_class = {}
        for entry in timetables:
            timetable_by_class.setdefault(entry.student_class, []).append(entry)
        return render(request, 'timetable/timetable.html', {
            'timetable_by_class': timetable_by_class,
            'classes': list(timetable_by_class.keys()),
            'no_class': False,
        })


@login_required_custom
def full_timetable_view(request):
    days = [day[0] for day in DAYS]

    # If student, only show their class's timetable
    if request.user.is_student and not request.user.is_admin and not request.user.is_teacher:
        # Try to find the student profile — by parent email, then by matching name
        student = (
            Student.objects.filter(parent__father_email=request.user.email).first()
            or Student.objects.filter(parent__mother_email=request.user.email).first()
            or Student.objects.filter(
                first_name=request.user.first_name,
                last_name=request.user.last_name
            ).first()
        )

        if student and student.student_class:
            timetables = list(TimeTable.objects.filter(
                student_class=student.student_class
            ).order_by('day', 'start_time'))
            timetable_by_class = {student.student_class: timetables}
            no_class = False
        else:
            timetable_by_class = {}
            no_class = True
    else:
        timetables = list(TimeTable.objects.all().order_by('student_class', 'day', 'start_time'))
        timetable_by_class = {}
        for entry in timetables:
            timetable_by_class.setdefault(entry.student_class, []).append(entry)
        no_class = False

    class_grids = []
    for class_name, entries in timetable_by_class.items():
        time_slots = sorted({(entry.start_time, entry.end_time) for entry in entries})
        slot_entries = {}
        for entry in entries:
            key = (entry.day, entry.start_time, entry.end_time)
            slot_entries.setdefault(key, []).append(entry)

        rows = []
        for start_time, end_time in time_slots:
            cells = []
            for day in days:
                cells.append(slot_entries.get((day, start_time, end_time), []))
            rows.append({
                'start_time': start_time,
                'end_time': end_time,
                'cells': cells,
            })

        class_grids.append({
            'class_name': class_name,
            'rows': rows,
        })

    return render(request, 'timetable/full-timetable.html', {
        'class_grids': class_grids,
        'days': days,
        'no_class': no_class,
    })


@teacher_required
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

@teacher_required
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

@teacher_required
def delete_timetable(request, pk):
    entry = get_object_or_404(TimeTable, pk=pk)
    entry.delete()
    messages.success(request, 'Timetable entry deleted successfully')
    next_url = request.GET.get('next')
    if next_url and next_url.startswith('/'):
        return redirect(next_url)
    return redirect('timetable_view')