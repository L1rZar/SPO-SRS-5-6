import json

from django.contrib import messages
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import SubjectForm, TaskForm
from .models import Subject, Task


def dashboard(request):
    today = timezone.localdate()
    tasks = Task.objects.select_related('subject')

    context = {
        'total_tasks': tasks.count(),
        'completed_tasks': tasks.filter(status='completed').count(),
        'in_progress_tasks': tasks.filter(status='in_progress').count(),
        'overdue_tasks': tasks.filter(
            due_date__lt=today
        ).exclude(status='completed').count(),
        'upcoming_tasks': tasks.filter(
            due_date__gte=today
        ).exclude(status='completed').order_by('due_date')[:5],
    }
    return render(request, 'planner/dashboard.html', context)


def task_list(request):
    tasks = Task.objects.select_related('subject')
    subjects = Subject.objects.all()
    return render(request, 'planner/tasks.html', {
        'tasks': tasks,
        'subjects': subjects,
        'form': TaskForm(),
    })


@require_POST
def task_create(request):
    form = TaskForm(request.POST)
    if not form.is_valid():
        return JsonResponse(
            {'errors': form.errors.get_json_data()},
            status=400,
        )

    task = form.save()
    task = Task.objects.select_related('subject').get(pk=task.pk)
    row_html = render_to_string(
        'planner/includes/task_row.html',
        {'task': task},
        request=request,
    )
    return JsonResponse({
        'message': 'Задание успешно добавлено.',
        'row_html': row_html,
    }, status=201)


def task_edit(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Задание успешно изменено.')
            return redirect('planner:tasks')
    else:
        form = TaskForm(instance=task)

    return render(request, 'planner/task_edit.html', {
        'form': form,
        'task': task,
    })


@require_POST
def task_change_status(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {'error': 'Не удалось прочитать данные запроса.'},
            status=400,
        )

    status = data.get('status')
    allowed_statuses = dict(Task.STATUS_CHOICES)
    if status not in allowed_statuses:
        return JsonResponse(
            {'error': 'Выбран неизвестный статус.'},
            status=400,
        )

    task.status = status
    task.save(update_fields=['status'])
    return JsonResponse({
        'message': 'Статус задания изменён.',
        'status': task.status,
        'status_label': task.get_status_display(),
    })


@require_POST
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.delete()
    return JsonResponse({'message': 'Задание успешно удалено.'})


def subject_list(request):
    subjects = Subject.objects.annotate(
        task_count=Count('tasks')
    ).order_by('name')

    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Дисциплина добавлена.')
            return redirect('planner:subjects')
    else:
        form = SubjectForm()

    return render(request, 'planner/subjects.html', {
        'subjects': subjects,
        'form': form,
    })


def api_console(request):
    return render(request, 'planner/api_console.html')
