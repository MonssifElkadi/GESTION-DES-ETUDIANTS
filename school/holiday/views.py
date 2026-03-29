from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Holiday
from home_auth.decorators import login_required_custom, admin_required

@login_required_custom
def holiday_list(request):
    holidays = Holiday.objects.all().order_by('date')
    return render(request, 'holidays/holidays.html', {'holidays': holidays})

@admin_required
def add_holiday(request):
    if request.method == 'POST':
        name        = request.POST.get('name')
        date        = request.POST.get('date')
        description = request.POST.get('description')
        Holiday.objects.create(name=name, date=date, description=description)
        messages.success(request, 'Holiday added successfully')
        return redirect('holiday_list')
    return render(request, 'holidays/add-holiday.html')

@admin_required
def edit_holiday(request, pk):
    holiday = get_object_or_404(Holiday, pk=pk)
    if request.method == 'POST':
        holiday.name        = request.POST.get('name')
        holiday.date        = request.POST.get('date')
        holiday.description = request.POST.get('description')
        holiday.save()
        messages.success(request, 'Holiday updated successfully')
        return redirect('holiday_list')
    return render(request, 'holidays/edit-holiday.html', {'holiday': holiday})

@admin_required
def delete_holiday(request, pk):
    holiday = get_object_or_404(Holiday, pk=pk)
    holiday.delete()
    messages.success(request, 'Holiday deleted successfully')
    return redirect('holiday_list')