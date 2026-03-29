from django.shortcuts import redirect

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_admin and not request.user.is_superuser:
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

def teacher_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not (request.user.is_teacher or request.user.is_admin or request.user.is_superuser):
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

def login_required_custom(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper
