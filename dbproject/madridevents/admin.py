from django.contrib import admin
from .models import Events  # Ensure this matches your model name

@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'start_time', 'end_time', 'location', 'image_url']

