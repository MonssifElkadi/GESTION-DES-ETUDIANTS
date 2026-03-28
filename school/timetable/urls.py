from django.urls import path
from . import views

urlpatterns = [
    path('', views.timetable_view, name='timetable_view'),
    path('add/', views.add_timetable, name='add_timetable'),
    path('edit/<int:pk>/', views.edit_timetable, name='edit_timetable'),
    path('delete/<int:pk>/', views.delete_timetable, name='delete_timetable'),
]