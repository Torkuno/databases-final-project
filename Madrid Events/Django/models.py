from django.db import models

class Events(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField() 
    end_time = models.TimeField()
    image_url = models.CharField(max_length=100)


class MongoDBModel(models.Model):
    # Fields for your MongoDB model
    name = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField() 
    end_time = models.TimeField()
    image_url = models.CharField(max_length=100)
    

    class Meta:
        # Set the database alias to 'mongodb'
        app_label = 'madridevents'
