from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import (
  F, Q, When, Case, Value, FloatField, IntegerField,
  Sum, Avg,
)
from .models import (
  Person, Company, Vehicle, Place, Trip, TripParams, TripInterval,
)
import json


class RequestView(TemplateView):
  template_name = "request.html"
  
  def get_context_data(self, **kwargs):
    self.extra_context = dict(results=json.dumps(self.get_result(), indent=2, default=str))
    return super().get_context_data(**kwargs)
  
  def get_result(self):
    result = {
      "this": 'is working variant of project'
    }
    queryset = TripInterval.objects.annotate(
      tm=F('timestamp'),
      spd=(F('path') / F('time')),
      drv=F('params__driver__name'),
      big_spd=Case(
        When(spd__gt=1, then=F('spd')),
        output_field=FloatField()
      ),
    ).aggregate(
      spd_sum=Sum('spd'),
      big_spd_sum=Sum('big_spd')
    )
    
    print(queryset)
    
    result['objects'] = list(queryset)
    
    return result
