from django import forms
from .models import Task, Tag


class TaskForm(forms.ModelForm):
    existing_tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Wybierz istniejące tagi",
    )
    new_tags = forms.CharField(
        required=False,
        label="Nowe tagi (oddziel przecinkami)",
    )

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "status",
            "deadline",
            "priority",
            "existing_tags",
            "new_tags",
        ]
