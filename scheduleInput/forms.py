from django import forms
from .models import ClassInput

class ClassInputForm(forms.ModelForm):
    class Meta:
        model = ClassInput
        fields = ['name', 'startTime', 'endTime', 'days', 'location']