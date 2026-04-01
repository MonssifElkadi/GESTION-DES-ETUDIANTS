from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser, PasswordResetRequest
from teacher.models import Teacher
from student.models import Student, Parent
from departement.models import Department


# ─── Login ────────────────────────────────────────────────────────────────────
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user_obj = CustomUser.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except CustomUser.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'authentication/login.html')


# ─── Register ─────────────────────────────────────────────────────────────────
def signup_view(request):
    departments = Department.objects.all()

    if request.method == 'POST':
        role          = request.POST.get('role')          # 'student' or 'teacher'
        first_name    = request.POST.get('first_name')
        last_name     = request.POST.get('last_name')
        email         = request.POST.get('email')
        password      = request.POST.get('password')
        confirm_pass  = request.POST.get('confirm_password')

        # — Validation —
        if password != confirm_pass:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'authentication/register.html', {'departments': departments})

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered.')
            return render(request, 'authentication/register.html', {'departments': departments})

        if role not in ('student', 'teacher'):
            messages.error(request, 'Please select a valid role.')
            return render(request, 'authentication/register.html', {'departments': departments})

        # — Role-specific data (validate before creating the user) —
        if role == 'teacher':
            teacher_id   = request.POST.get('teacher_id')
            gender       = request.POST.get('teacher_gender') or 'Male'
            dob          = request.POST.get('teacher_date_of_birth')
            mobile       = request.POST.get('teacher_mobile_number', '')
            dept_id      = request.POST.get('department')
            joining_date = request.POST.get('teacher_joining_date')

            if not dob or not joining_date:
                messages.error(request, 'Date of birth and joining date are required for teachers.')
                return render(request, 'authentication/register.html', {'departments': departments})

        elif role == 'student':
            student_id       = request.POST.get('student_id')
            gender           = request.POST.get('student_gender') or 'Male'
            dob              = request.POST.get('student_date_of_birth')
            student_class    = request.POST.get('student_class', '')
            mobile           = request.POST.get('student_mobile_number', '')
            admission_number = request.POST.get('admission_number', '')
            section          = request.POST.get('section', '')
            joining_date     = request.POST.get('student_joining_date')
            father_name      = request.POST.get('father_name', '')
            father_mobile    = request.POST.get('father_mobile', '')
            father_email     = request.POST.get('father_email', email)
            mother_name      = request.POST.get('mother_name', '')
            mother_mobile    = request.POST.get('mother_mobile', '')
            mother_email     = request.POST.get('mother_email', '')
            address          = request.POST.get('present_address', '')

            if not dob or not joining_date:
                messages.error(request, 'Date of birth and joining date are required for students.')
                return render(request, 'authentication/register.html', {'departments': departments})

        # — Create CustomUser —
        username = email.split('@')[0]
        # make username unique if it already exists
        base_username = username
        counter = 1
        while CustomUser.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_teacher=(role == 'teacher'),
            is_student=(role == 'student'),
        )

        # — Create linked profile —
        if role == 'teacher':
            if not teacher_id:
                teacher_id = f'T-{user.pk}'

            department    = Department.objects.filter(pk=dept_id).first()

            Teacher.objects.create(
                first_name=first_name,
                last_name=last_name,
                teacher_id=teacher_id,
                gender=gender,
                date_of_birth=dob,
                email=email,
                mobile_number=mobile,
                department=department,
                joining_date=joining_date,
            )

        elif role == 'student':
            if not student_id:
                student_id = f'S-{user.pk}'

            parent = Parent.objects.create(
                father_name=father_name,
                father_mobile=father_mobile,
                father_email=father_email,
                mother_name=mother_name,
                mother_mobile=mother_mobile,
                mother_email=mother_email,
                present_address=address,
                permanent_address=address,
            )
            Student.objects.create(
                first_name=first_name,
                last_name=last_name,
                student_id=student_id,
                gender=gender,
                date_of_birth=dob,
                student_class=student_class,
                mobile_number=mobile,
                admission_number=admission_number,
                section=section,
                joining_date=joining_date,
                parent=parent,
            )

        messages.success(request, f'Account created as {role.capitalize()}! You can now log in.')
        return redirect('login')

    return render(request, 'authentication/register.html', {'departments': departments})



# ─── Logout ───────────────────────────────────────────────────────────────────
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


# ─── Forgot Password ──────────────────────────────────────────────────────────
def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            reset_req = PasswordResetRequest.objects.create(user=user, email=email)
            reset_req.send_reset_email()
            messages.success(request, 'A password reset link has been sent to your email.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'No account found with that email.')
    return render(request, 'authentication/forgot-password.html')


# ─── Reset Password ───────────────────────────────────────────────────────────
def reset_password_view(request, token):
    try:
        reset_req = PasswordResetRequest.objects.get(token=token)
    except PasswordResetRequest.DoesNotExist:
        messages.error(request, 'Invalid or expired reset link.')
        return redirect('forgot-password')

    if not reset_req.is_valid():
        messages.error(request, 'This reset link has expired.')
        return redirect('forgot-password')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        else:
            user = reset_req.user
            user.set_password(new_password)
            user.save()
            reset_req.delete()
            messages.success(request, 'Password reset successfully. You can now log in.')
            return redirect('login')
    return render(request, 'authentication/reset_password.html', {'token': token})
