from django.db import models

# Define a Django model named 'Events' representing events in a database
class Events(models.Model):
    # Define fields for the model with various data types
    name = models.CharField(max_length=100)  # Event name, limited to 100 characters
    date = models.DateField()  # Event date
    start_time = models.TimeField()  # Event start time
    end_time = models.TimeField()  # Event end time
    location = models.CharField(max_length=100)  # Event location, limited to 100 characters
    image_url = models.CharField(max_length=100)  # URL for the event image

    # Define meta-information for the 'Events' model
    class Meta:
        db_table = 'events'  # Specify the database table name for the model
