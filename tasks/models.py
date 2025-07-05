from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tags")

    class Meta:
        unique_together = ("name", "user")

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("low", "Niski"),
        ("medium", "Średni"),
        ("high", "Wysoki"),
    ]

    STATUS_CHOICES = [
        ("todo", "Do zrobienia"),
        ("in_progress", "W trakcie"),
        ("done", "Zrobione"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")
    created_at = models.DateTimeField(auto_now_add=True)

    deadline = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="low")

    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title
