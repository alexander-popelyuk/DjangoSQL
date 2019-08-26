from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import (
  F, Q, When, Case, Value, FloatField, IntegerField,
  Sum, Avg, Count, Window, Min, Max, Subquery
)
from .models import (
  Person, Company, Vehicle, Place, Trip, TripParams, TripInterval,
)
import json
from django.db.models.expressions import (
  RawSQL, OrderBy
)
from django.db.models.functions import RowNumber
from random import random


class RequestView(TemplateView):
  template_name = "request.html"
  
  def get_context_data(self, **kwargs):
    result = self.get_result()
    self.extra_context = dict(results=json.dumps(result, indent=2, default=str))
    return super().get_context_data(**kwargs)
  
  def get_result(self):
    result = TripInterval.sa.query().all()
    
    
    
    return result
    
    
  def get_result2(self):
    #self.insert_data()

    # id_row = Window(RowNumber(), order_by=F('id').asc())
    # time_row = Window(RowNumber(), partition_by=F('time'), order_by=F('id').asc())
    #
    # TripInterval.objects.annotate(
    #   time_grp=id_row - time_row
    # ).values('time_grp'
    # )
    #
    # queryset = TripInterval.objects.annotate(
    #   time_grp=id_row - time_row
    # ).values(
    #   'time', 'time_grp'
    # ).annotate(
    #   start_id=Min('id'), end_id=Max('id')
    # ).order_by(
    #  'start_id'
    # ).values(
    #   'time', 'start_id', 'end_id'
    # )

    #SELECT "request_tripinterval"."id", "request_tripinterval"."timestamp", "request_tripinterval"."params_id", "request_tripinterval"."trip_id",
    #  "request_tripinterval"."time", "request_tripinterval"."path" FROM "request_tripinterval"
    #SELECT "request_tripinterval"."id", ROW_NUMBER() OVER (ORDER BY "request_tripinterval"."id" ASC) AS "num" FROM "request_tripinterval"
    return [item for item in queryset.iterator()]
  
  def _get_result(self):
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
  
  
  def insert_data(self):
    params = TripParams.objects.get(id=1)
    trip = Trip.objects.get(id=1)
    blk_len = 0
    for i in range(100):
      if blk_len:
        blk_len -= 1
      else:
        blk_len = round(random() * 10)
        time = round(random() * 100)
        
      TripInterval.objects.create(
        params=params,
        trip=trip,
        time=time,
        path=round(random() * 100)
      )