from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Subject
from departement.models import Department
from teacher.models import Teacher

def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'subjects/subjects.html', {'subjects': subjects})

def add_subject(request):
    departments = Department.objects.all()
    teachers    = Teacher.objects.all()
    if request.method == 'POST':
        name          = request.POST.get('name')
        subject_code  = request.POST.get('subject_code')
        department_id = request.POST.get('department')
        teacher_id    = request.POST.get('teacher')
        department    = get_object_or_404(Department, pk=department_id)
        teacher       = Teacher.objects.filter(pk=teacher_id).first()
        Subject.objects.create(
            name=name,
            subject_code=subject_code,
            department=department,
            teacher=teacher,
        )
        messages.success(request, 'Subject added successfully')
        return redirect('subject_list')
    return render(request, 'subjects/add-subject.html', {'departments': departments, 'teachers': teachers})

def edit_subject(request, pk):
    subject     = get_object_or_404(Subject, pk=pk)
    departments = Department.objects.all()
    teachers    = Teacher.objects.all()
    if request.method == 'POST':
        subject.name         = request.POST.get('name')
        subject.subject_code = request.POST.get('subject_code')
        department_id        = request.POST.get('department')
        teacher_id           = request.POST.get('teacher')
        subject.department   = get_object_or_404(Department, pk=department_id)
        subject.teacher      = Teacher.objects.filter(pk=teacher_id).first()
        subject.save()
        messages.success(request, 'Subject updated successfully')
        return redirect('subject_list')
    return render(request, 'subjects/edit-subject.html', {'subject': subject, 'departments': departments, 'teachers': teachers})

def delete_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    subject.delete()
    messages.success(request, 'Subject deleted successfully')
    return redirect('subject_list')