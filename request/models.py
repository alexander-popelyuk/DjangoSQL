from django.db import models

class Person(models.Model):
  name = models.CharField(max_length=32)
  age = models.IntegerField()
  
  def __str__(self):
    return self.name

class Company(models.Model):
  name = models.CharField(max_length=32)
  manager = models.ForeignKey(Person, on_delete=models.CASCADE)
  
  def __str__(self):
    return self.name
  
class Vehicle(models.Model):
  name = models.CharField(max_length=32)
  color = models.CharField(max_length=16)
  company = models.ForeignKey(Company, on_delete=models.CASCADE)
  
  def __str__(self):
    return self.name

class Place(models.Model):
  name = models.CharField(max_length=32)
  
  def __str__(self):
    return self.name

class Trip(models.Model):
  vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
  start = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='start_trips_set')
  target = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='target_trips_set')
  
  def __str__(self):
    return "%s => %s" % (self.start.name, self.target.name)
  
class TripParams(models.Model):
  min_allowed_speed = models.FloatField()
  max_allowed_speed = models.FloatField()
  allowed_passengers_count = models.IntegerField()
  driver = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='driver_trip_params')
  passengers = models.ManyToManyField(Person, related_name='passengers_trip_params')

  def __str__(self):
    return "drv=%s: min=%d, max=%d, alw_psg_cnt=%d" % (
      self.driver.name, self.min_allowed_speed, self.max_allowed_speed, self.allowed_passengers_count
    )

class TripInterval(models.Model):
  timestamp = models.DateTimeField(auto_now=True)
  params = models.ForeignKey(TripParams, on_delete=models.CASCADE)
  trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
  path = models.FloatField()
  time = models.FloatField()
  
  def __str__(self):
    return "%s: %s, (%s), path=%.3f, time=%.3f" % (
      self.timestamp, self.params.driver.name, self.trip, self.path, self.time
    )
