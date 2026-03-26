from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser, PasswordResetRequest


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
            if user.is_admin or user.is_staff or user.is_superuser:
                return redirect('dashboard')
            elif user.is_teacher:
                return redirect('dashboard')
            elif user.is_student:
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid user role')
                return redirect('index')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'authentication/login.html')


# ─── Register ─────────────────────────────────────────────────────────────────
def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('signup')

        username = email.split('@')[0]
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        messages.success(request, 'Account created! You can now log in.')
        return redirect('login')
    return render(request, 'authentication/register.html')


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
