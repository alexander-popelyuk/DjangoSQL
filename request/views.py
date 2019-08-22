from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import (
  F, Q, When, Case, Value, FloatField, IntegerField,
  Sum, Avg, Count
)
from .models import (
  Person, Company, Vehicle, Place, Trip, TripParams, TripInterval,
)
import json


class RequestView(TemplateView):
  template_name = "request.html"
  
  def get_context_data(self, **kwargs):
    result = self.get_result()
    self.extra_context = dict(results=json.dumps(result, indent=2, default=str))
    return super().get_context_data(**kwargs)
  
  def get_result(self):
    queryset = TripInterval.objects.annotate(
      **self.get_annotation()
    ).aggregate(
      spd_sum=Sum('spd'),
      big_spd_sum=Sum('big_spd'),
      spd_cnt=Count('spd'),
      big_spd_cnt=Count('big_spd')
    )
    
    result = dict(queryset)
    
    return result

  def get_annotation(self):
    return {
      'tm': F('timestamp'),
      'spd':(F('path') / F('time')),
      'drv': F('params__driver__name'),
      'big_spd': Case(
        When(spd__gt=1, then=F('spd')),
        output_field=FloatField()
      ),
    }