from django.db import models

class User(models.Model):
  name = models.CharField(max_length=32)

class Session(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

class Request(models.Model):
  session = models.ForeignKey(Session, on_delete=models.CASCADE)
  timestamp = models.DateTimeField(auto_now=True)
  action = models.CharField(max_length=32)
  params = models.CharField(max_length=2048)

class Company(models.Model):
  manager = models.ForeignKey(User, on_delete=models.CASCADE)

class Vehicle(models.Model):
  company = models.ForeignKey(Company, on_delete=models.CASCADE)
  timestamp = models.DateTimeField(auto_now=True)

class Trip(models.Model):
  vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
  timestamp = models.DateTimeField(auto_now=True)
  path = models.FloatField()
  time = models.FloatField()
