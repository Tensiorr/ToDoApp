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
        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['existing_tags'].queryset = Tag.objects.filter(user=user)
