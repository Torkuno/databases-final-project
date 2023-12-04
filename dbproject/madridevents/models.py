from django.db import models

class Events(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=100)
    image_url = models.CharField(max_length=100)

    class Meta:
        db_table = 'events'
