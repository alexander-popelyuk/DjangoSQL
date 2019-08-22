from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import (
  F, Q, When, Case, Value, FloatField, IntegerField
)
from .models import (
  Person, Company, Vehicle, Place, Trip, TripParams, TripInterval,
)
import json


class RequestView(TemplateView):
  template_name = "request.html"
  
  def get_context_data(self, **kwargs):
    self.extra_context = dict(results=json.dumps(self.get_result(), indent=2))
    return super().get_context_data(**kwargs)
  
  def get_result(self):
    result = {
      "this": 'is working variant of project'
    }
    
    return result
