from datetime import datetime
from urllib.parse import urlencode

from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.decorators import login_required

from .models import Task, Status, Worker
from .utils import task_is_expired


@login_required(redirect_field_name='')
def tasks_list(request):

    tasks = Task.objects.filter(worker__user=request.user)

    for task in tasks:
        if not task.actual_end_date and task_is_expired(task):
            task.status = Status.objects.get(text='Просрочено')
            task.save()

    data = request.GET
    try:
        status_id = int(data.get('status'))
    except:
        status_id = None    
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    if status_id:
        tasks = tasks.filter(status__id=int(status_id))
    if start_date:
        year, month, day = [int(d) for d in start_date.split('-')]
        start_date = datetime(year=year, month=month, day=day, hour=0, minute=0)
    if end_date:
        year, month, day = [int(d) for d in end_date.split('-')]
        end_date = datetime(year=year, month=month, day=day, hour=23, minute=59)

    if start_date and end_date:
        if start_date < end_date:
            tasks = tasks.filter(expected_end_date__range=(start_date, end_date))
    elif start_date:
        tasks = tasks.filter(expected_end_date__gte=start_date)
    elif end_date:
        tasks = tasks.filter(expected_end_date__lte=end_date)

    page = data.get('page', 1) if data.get('page', 1) else 1
    paginator = Paginator(tasks, 10)

    try:
        tasks = paginator.page(page)
    except EmptyPage:
        tasks = paginator.page(1)

    context = {
        'tasks': tasks,
        'statuses': Status.objects.all(),
        'selected_status_id': status_id,
        'start_date': start_date.strftime('%Y-%m-%d') if start_date else None,
        'end_date': end_date.strftime('%Y-%m-%d') if end_date else None,
    }

    return render(request, 'tasks/tasks_list.html', context)


@login_required(redirect_field_name='')
def change_status_task(request, pk):

    task = Task.objects.get(id=pk)

    if task_is_expired(task):
        task.status = Status.objects.get(text='Просрочено')
    elif task.status.text == 'Выполняется':
        task.status = Status.objects.get(text='Завершено')
    elif task.status.text == 'Завершено':
        task.status = Status.objects.get(text='Выполняется')

    task.save()

    return redirect(reverse('tasks_list') +'?'+ urlencode(request.GET))


@login_required(redirect_field_name='')
def create_task(request):

    context = {}

    if request.method == 'POST':
        data = request.POST
        text = data['text'].strip()
        contact = data['contact'].strip()
        
        date, time = data['expected_end_date'].split('T')
        year, month, day = [int(d) for d in date.split('-')]
        hour, minute = [int(t) for t in time.split(':')]
        expected_end_date = datetime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,

        )

        now = datetime.now()

        if now < expected_end_date:
            Task.objects.create(
                worker=Worker.objects.get(user=request.user),
                text=text,
                expected_end_date=expected_end_date,
                contact=contact if contact else None
            )

            return redirect('tasks_list')
        
        context['validation_error'] = True

    return render(request, 'tasks/create_task.html', context)


@login_required(redirect_field_name='')
def delete_task(request, pk):

    task = Task.objects.get(id=pk)
    task.delete()

    return redirect(reverse('tasks_list') +'?'+ urlencode(request.GET))