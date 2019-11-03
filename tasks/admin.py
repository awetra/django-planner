from django.contrib import admin

from .models import Profession, Worker, Status, Task


@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Profession._meta.fields]


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Worker._meta.fields]


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Status._meta.fields]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Task._meta.fields]