from django import forms
from .models import Events

class EventForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ['name', 'date', 'start_time', 'end_time', 'location', 'image_url']
