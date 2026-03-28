from django.urls import path
from . import views

urlpatterns = [
    path('', views.holiday_list, name='holiday_list'),
    path('add/', views.add_holiday, name='add_holiday'),
    path('edit/<int:pk>/', views.edit_holiday, name='edit_holiday'),
    path('delete/<int:pk>/', views.delete_holiday, name='delete_holiday'),
]