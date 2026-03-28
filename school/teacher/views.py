from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Teacher
from departement.models import Department

def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers/teachers.html', {'teachers': teachers})

def add_teacher(request):
    departments = Department.objects.all()
    if request.method == 'POST':
        first_name    = request.POST.get('first_name')
        last_name     = request.POST.get('last_name')
        teacher_id    = request.POST.get('teacher_id')
        gender        = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        email         = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        address       = request.POST.get('address')
        joining_date  = request.POST.get('joining_date')
        department_id = request.POST.get('department')
        teacher_image = request.FILES.get('teacher_image')
        department    = Department.objects.get(pk=department_id) if department_id else None

        Teacher.objects.create(
            first_name=first_name,
            last_name=last_name,
            teacher_id=teacher_id,
            gender=gender,
            date_of_birth=date_of_birth,
            email=email,
            mobile_number=mobile_number,
            address=address,
            joining_date=joining_date,
            department=department,
            teacher_image=teacher_image,
        )
        messages.success(request, 'Teacher added successfully')
        return redirect('teacher_list')
    return render(request, 'teachers/add-teacher.html', {'departments': departments})

def view_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    return render(request, 'teachers/teacher-details.html', {'teacher': teacher})

def edit_teacher(request, pk):
    teacher     = get_object_or_404(Teacher, pk=pk)
    departments = Department.objects.all()
    if request.method == 'POST':
        teacher.first_name    = request.POST.get('first_name')
        teacher.last_name     = request.POST.get('last_name')
        teacher.teacher_id    = request.POST.get('teacher_id')
        teacher.gender        = request.POST.get('gender')
        teacher.date_of_birth = request.POST.get('date_of_birth')
        teacher.email         = request.POST.get('email')
        teacher.mobile_number = request.POST.get('mobile_number')
        teacher.address       = request.POST.get('address')
        teacher.joining_date  = request.POST.get('joining_date')
        department_id         = request.POST.get('department')
        teacher.department    = Department.objects.get(pk=department_id) if department_id else None
        if request.FILES.get('teacher_image'):
            teacher.teacher_image = request.FILES.get('teacher_image')
        teacher.save()
        messages.success(request, 'Teacher updated successfully')
        return redirect('teacher_list')
    return render(request, 'teachers/edit-teacher.html', {'teacher': teacher, 'departments': departments})

def delete_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    teacher.delete()
    messages.success(request, 'Teacher deleted successfully')
    return redirect('teacher_list')