from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'location', 'is_active']
        # On utilise des widgets pour améliorer l'apparence des champs
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'input-field'}),
            'name': forms.TextInput(attrs={'class': 'input-field'}),
            'location': forms.TextInput(attrs={'class': 'input-field'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'input-field'}),
        }
