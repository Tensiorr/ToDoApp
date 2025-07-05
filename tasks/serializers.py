from rest_framework import serializers
from .models import Task, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class TaskSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )
    tag_list = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "created_at",
            "deadline",
            "priority",
            "tags",
            "tag_list",
        ]
        read_only_fields = ["created_at"]
        extra_kwargs = {
            "title": {"help_text": "Tytuł zadania"},
            "description": {"help_text": "Opcjonalny opis"},
            "status": {"help_text": "Czy zadanie zostało ukończone"},
            "deadline": {"help_text": "Termin końcowy zadania"},
            "priority": {"help_text": "Priorytet zadania"},
        }

        def get_tag_list(self, obj):
            return [tag.name for tag in obj.tags.all()]

        def create(self, validated_data):
            tags_data = validated_data.pop('tags', [])
            task = Task.objects.create(**validated_data, user=self.context['request'].user)

            for tag_name in tags_data:
                tag, _ = Tag.objects.get_or_create(name=tag_name, user=task.user)
                task.tags.add(tag)

            return task

        def update(self, instance, validated_data):
            tags_data = validated_data.pop('tags', None)
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            if tags_data is not None:
                instance.tags.clear()
                for tag_name in tags_data:
                    tag, _ = Tag.objects.get_or_create(name=tag_name, user=instance.user)
                    instance.tags.add(tag)

            instance.save()
            return instance
