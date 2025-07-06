# from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from .models import Task, Tag
from .serializers import TaskSerializer, TagSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TaskForm


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
    tasks = Task.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "tasks_list.html", {"tasks": tasks})


@login_required
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        form.fields["existing_tags"].queryset = Tag.objects.filter(user=request.user)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()

            existing_tags = form.cleaned_data["existing_tags"]
            for tag in existing_tags:
                task.tags.add(tag)

            new_tags_str = form.cleaned_data["new_tags"]
            if new_tags_str:
                new_tag_names = [
                    t.strip() for t in new_tags_str.split(",") if t.strip()
                ]
                for name in new_tag_names:
                    tag, _ = Tag.objects.get_or_create(name=name, user=request.user)
                    task.tags.add(tag)

            return redirect("tasks_list")
    else:
        form = TaskForm()
        form.fields["existing_tags"].queryset = Tag.objects.filter(user=request.user)

    return render(request, "add_task.html", {"form": form})


def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()

            existing_tags = form.cleaned_data["existing_tags"]
            task.tags.set(existing_tags)

            new_tags_str = form.cleaned_data["new_tags"]
            new_tag_names = [
                name.strip() for name in new_tags_str.split(",") if name.strip()
            ]
            for tag_name in new_tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name, user=request.user)
                task.tags.add(tag)

            return redirect("tasks_list")
    else:
        initial = {"existing_tags": task.tags.all(), "new_tags": ""}
        form = TaskForm(instance=task, initial=initial)
    return render(request, "tasks/edit_task.html", {"form": form, "task": task})
