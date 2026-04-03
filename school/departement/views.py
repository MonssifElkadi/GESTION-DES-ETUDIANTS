from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Department
from home_auth.decorators import admin_required
from teacher.models import Teacher

@admin_required
def departement_list(request):
    departments = Department.objects.all()
    return render(request,'departments/department.html' , {'departments' : departments})

@admin_required
def add_department(request):
    teachers = Teacher.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        head_teacher_id = request.POST.get('head_teacher')
        
        head_teacher = None
        if head_teacher_id:
             head_teacher = get_object_or_404(Teacher, pk=head_teacher_id)
             
        Department.objects.create(
            name=name,
            description=description,
            head_teacher=head_teacher
        )
        messages.success(request, 'Department added successfully')
        return redirect('department_list')
    return render(request,'departments/add-department.html', {'teachers': teachers})

@admin_required
def edit_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    teachers = Teacher.objects.all()
    if request.method == 'POST':
        department.name = request.POST.get('name')
        department.description = request.POST.get('description')
        head_teacher_id = request.POST.get('head_teacher')
        
        if head_teacher_id:
             department.head_teacher = get_object_or_404(Teacher, pk=head_teacher_id)
        else:
             department.head_teacher = None
             
        department.save()
        messages.success(request, 'Department updated successfully')
        return redirect('department_list')
    return render(request, 'departments/edit-department.html', {'department': department, 'teachers': teachers})

@admin_required
def delete_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    department.delete()
    messages.success(request, 'Department deleted successfully')
    return redirect('department_list')
