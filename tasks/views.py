from rest_framework import viewsets, permissions, filters
from .models import Task, Tag
from .serializers import TaskSerializer, TagSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from django.views.decorators.http import require_POST
from datetime import date
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Count
import json


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user).order_by("name")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ["status", "priority", "deadline", "tags"]
    ordering_fields = ["created_at", "title", "priority", "deadline"]
    search_fields = ["title", "description"]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@login_required
def tasks_list(request):
    tags = (
        Tag.objects.filter(user=request.user)
        .annotate(task_count=Count("task"))
        .filter(task_count__gt=0)
    )
    selected_tags = request.GET.getlist("tags")
    tasks = Task.objects.filter(user=request.user).order_by("-created_at")
    today = date.today()

    if selected_tags:
        for tag_name in selected_tags:
            tasks = tasks.filter(tags__name=tag_name)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("tasks_partial.html", {"tasks": tasks, "today": today})
        return JsonResponse({"html": html})

    return render(
        request,
        "tasks_list.html",
        {"tasks": tasks, "tags": tags, "selected_tags": selected_tags, "today": today},
    )


@login_required
def delete_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id, user=request.user)
    tag.delete()
    return redirect("tasks:task_list")


@login_required
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()

            existing_tags = form.cleaned_data['existing_tags']
            task.tags.set(existing_tags)

            new_tags_str = form.cleaned_data.get('new_tags')
            if new_tags_str:
                new_tags_list = [t.strip() for t in new_tags_str.split(",") if t.strip()]
                for tag_name in new_tags_list:
                    tag_obj, created = Tag.objects.get_or_create(name=tag_name, user=request.user)
                    task.tags.add(tag_obj)

            return redirect('tasks_list')
    else:
        form = TaskForm(user=request.user)

    tags = Tag.objects.filter(user=request.user)
    return render(request, "add_task.html", {
        "form": form,
        "tags": tags,
        "is_edit": False,
    })


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            updated_task = form.save(commit=False)
            updated_task.user = request.user
            updated_task.save()

            existing_tags = form.cleaned_data['existing_tags']
            updated_task.tags.set(existing_tags)

            new_tags_str = form.cleaned_data.get('new_tags')
            if new_tags_str:
                new_tags_list = [t.strip() for t in new_tags_str.split(",") if t.strip()]
                for tag_name in new_tags_list:
                    tag_obj, created = Tag.objects.get_or_create(name=tag_name, user=request.user)
                    updated_task.tags.add(tag_obj)

            return redirect('tasks_list')
    else:
        form = TaskForm(instance=task, user=request.user)
        form.fields['existing_tags'].initial = task.tags.all()

    tags = Tag.objects.filter(user=request.user)
    return render(request, "edit_task.html", {
        "form": form,
        "tags": tags,
        "task": task,
        "is_edit": True,
    })


@login_required
@require_POST
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect("tasks_list")


@require_POST
@login_required
def update_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    try:
        data = json.loads(request.body)
        new_status = data.get("status")
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Błędny JSON"})

    if new_status in ["to_do", "in_progress", "done"]:
        task.status = new_status
        task.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error": "Nieprawidłowy status"})
