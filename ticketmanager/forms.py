from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Event, Ticket

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'location', 'is_active']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'input-field'}),
            'name': forms.TextInput(attrs={'class': 'input-field'}),
            'location': forms.TextInput(attrs={'class': 'input-field'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'input-field'}),
        }

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['ticket_type', 'price', 'quantity_available', 'is_active']
        widgets = {
            'ticket_type': forms.Select(attrs={'class': 'input-field'}),
            'price': forms.NumberInput(attrs={'class': 'input-field', 'step': '0.01'}),
            'quantity_available': forms.NumberInput(attrs={'class': 'input-field'}),
            'is_active': forms.CheckboxInput(),
        }


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
