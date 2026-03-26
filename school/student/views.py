from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Parent


def student_list(request):
    student_list = Student.objects.all()
    return render(request, 'students/students.html', {'student_list': student_list})


def add_student(request):
    if request.method == 'POST':
        # Create Parent first
        parent = Parent.objects.create(
            father_name=request.POST['father_name'],
            father_occupation=request.POST['father_occupation'],
            father_mobile=request.POST['father_mobile'],
            father_email=request.POST['father_email'],
            mother_name=request.POST['mother_name'],
            mother_occupation=request.POST['mother_occupation'],
            mother_mobile=request.POST['mother_mobile'],
            mother_email=request.POST['mother_email'],
            present_address=request.POST['present_address'],
            permanent_address=request.POST['permanent_address'],
        )
        # Create Student linked to parent
        student = Student(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            student_id=request.POST['student_id'],
            gender=request.POST['gender'],
            date_of_birth=request.POST['date_of_birth'],
            student_class=request.POST['student_class'],
            joining_date=request.POST['joining_date'],
            mobile_number=request.POST['mobile_number'],
            admission_number=request.POST['admission_number'],
            section=request.POST['section'],
            parent=parent,
        )
        if 'student_image' in request.FILES:
            student.student_image = request.FILES['student_image']
        student.save()
        return redirect('student_list')
    return render(request, 'students/add-student.html')


def edit_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    if request.method == 'POST':
        student.first_name = request.POST['first_name']
        student.last_name = request.POST['last_name']
        student.gender = request.POST['gender']
        student.date_of_birth = request.POST['date_of_birth']
        student.student_class = request.POST['student_class']
        student.joining_date = request.POST['joining_date']
        student.mobile_number = request.POST['mobile_number']
        student.admission_number = request.POST['admission_number']
        student.section = request.POST['section']
        if 'student_image' in request.FILES:
            student.student_image = request.FILES['student_image']
        student.save()
        # Update parent info
        student.parent.father_name = request.POST['father_name']
        student.parent.father_occupation = request.POST['father_occupation']
        student.parent.father_mobile = request.POST['father_mobile']
        student.parent.father_email = request.POST['father_email']
        student.parent.mother_name = request.POST['mother_name']
        student.parent.mother_occupation = request.POST['mother_occupation']
        student.parent.mother_mobile = request.POST['mother_mobile']
        student.parent.mother_email = request.POST['mother_email']
        student.parent.present_address = request.POST['present_address']
        student.parent.permanent_address = request.POST['permanent_address']
        student.parent.save()
        return redirect('student_list')
    return render(request, 'students/edit-student.html', {'student': student})


def view_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    return render(request, 'students/student-details.html', {'student': student})


def delete_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    if request.method == 'POST':
        student.parent.delete()  # deletes student too (CASCADE)
    return redirect('student_list')
