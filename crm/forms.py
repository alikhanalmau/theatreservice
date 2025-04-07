from django import forms
from theatre.models import Event,ExcursionOrder, ExcursionSlot, TicketOrder
from django.contrib.auth import get_user_model

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'image']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class ExcursionForm(forms.ModelForm):
    class Meta:
        model = ExcursionOrder
        fields = ['user', 'slot', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

class ExcursionSlotForm(forms.ModelForm):
    class Meta:
        model = ExcursionSlot
        fields = ['date', 'time', 'capacity']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
        }



class TicketOrderForm(forms.ModelForm):
    class Meta:
        model = TicketOrder
        fields = ['user', 'event', 'count', 'status', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 2}),
        }

User = get_user_model()
class UserRoleForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['role']