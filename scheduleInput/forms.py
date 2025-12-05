from django import forms
from .models import ClassInput

class ClassInputForm(forms.ModelForm):
    days = forms.MultipleChoiceField(
        choices=ClassInput.DAY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = ClassInput
        fields = ['name', 'startTime', 'endTime', 'days', 'location']
        widgets = {
            'startTime': forms.TimeInput(attrs={'type': 'time'}),
            'endTime': forms.TimeInput(attrs={'type': 'time'}),
        }
