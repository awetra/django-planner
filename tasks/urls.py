from django.urls import path

from . import views


urlpatterns = [
    path('', views.tasks_list, name='tasks_list'),
    path('task/create/', views.create_task, name='create_task'),
    path('task/<int:pk>/delete/', views.delete_task, name='delete_task'),
    path('task/<int:pk>/change-status/', views.change_status_task, name='change_status_task'),
]