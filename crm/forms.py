from django import forms
from theatre.models import Event,ExcursionOrder, TicketOrder
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