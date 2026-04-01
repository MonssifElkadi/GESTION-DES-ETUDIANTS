from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Exam, ExamResult
from subject.models import Subject
from student.models import Student
from home_auth.decorators import login_required_custom, teacher_required

@login_required_custom
def exam_list(request):
    exams = Exam.objects.all().order_by('date')
    return render(request, 'exams/exams.html', {'exams': exams})

@teacher_required
def add_exam(request):
    subjects = Subject.objects.all()
    if request.method == 'POST':
        name          = request.POST.get('name')
        subject_id    = request.POST.get('subject')
        date          = request.POST.get('date')
        start_time    = request.POST.get('start_time')
        student_class = request.POST.get('student_class')
        subject       = get_object_or_404(Subject, pk=subject_id)
        Exam.objects.create(
            name=name,
            subject=subject,
            date=date,
            start_time=start_time,
            student_class=student_class,
        )
        messages.success(request, 'Exam added successfully')
        return redirect('exam_list')
    return render(request, 'exams/add-exam.html', {'subjects': subjects})

@teacher_required
def edit_exam(request, pk):
    exam     = get_object_or_404(Exam, pk=pk)
    subjects = Subject.objects.all()
    if request.method == 'POST':
        exam.name          = request.POST.get('name')
        exam.date          = request.POST.get('date')
        exam.start_time    = request.POST.get('start_time')
        exam.student_class = request.POST.get('student_class')
        subject_id         = request.POST.get('subject')
        exam.subject       = get_object_or_404(Subject, pk=subject_id)
        exam.save()
        messages.success(request, 'Exam updated successfully')
        return redirect('exam_list')
    return render(request, 'exams/edit-exam.html', {'exam': exam, 'subjects': subjects})

@teacher_required
def delete_exam(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    exam.delete()
    messages.success(request, 'Exam deleted successfully')
    return redirect('exam_list')

@teacher_required
def add_result(request, pk):
    exam     = get_object_or_404(Exam, pk=pk)
    students = Student.objects.filter(student_class=exam.student_class).order_by('first_name', 'last_name')
    results  = ExamResult.objects.filter(exam=exam)
    if request.method == 'POST':
        student_id = request.POST.get('student')
        marks      = request.POST.get('marks')
        student    = get_object_or_404(
            Student,
            pk=student_id,
            student_class=exam.student_class,
        )
        result, created = ExamResult.objects.update_or_create(
            exam=exam, 
            student=student, 
            defaults={'marks': float(marks)}
        )
        messages.success(request, 'Result saved successfully')
        return redirect('add_result', pk=exam.pk)
    return render(request, 'exams/exam-results.html', {'exam': exam, 'students': students, 'results': results})