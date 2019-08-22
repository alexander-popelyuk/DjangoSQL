from django.contrib import admin
from .models import (
  Person, Company, Vehicle, Place, Trip, TripParams, TripInterval,
)

admin.site.register(Person)
admin.site.register(Company)
admin.site.register(Vehicle)
admin.site.register(Place)
admin.site.register(Trip)
admin.site.register(TripParams)
admin.site.register(TripInterval)
