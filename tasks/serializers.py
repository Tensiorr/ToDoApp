from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "status", "created_at", "deadline", "priority"]
        read_only_fields = ["created_at"]
        extra_kwargs = {
            "title": {"help_text": "Tytuł zadania"},
            "description": {"help_text": "Opcjonalny opis"},
            "status": {"help_text": "Czy zadanie zostało ukończone"},
            "deadline": {"help_text": "Termin końcowy zadania"},
            "priority": {"help_text": "Priorytet zadania"},
        }
