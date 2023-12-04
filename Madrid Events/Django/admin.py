from django.contrib import admin
from .models import Events, MongoDBModel



admin.site.register(Events)
admin.site.register(MongoDBModel)