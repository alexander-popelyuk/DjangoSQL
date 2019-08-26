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
from django.db import connection


class RequestView(TemplateView):
  template_name = "request.html"
  
  def get_context_data(self, **kwargs):
    result = self.get_result()
    self.extra_context = dict(results=json.dumps(result, indent=2, default=str))
    return super().get_context_data(**kwargs)
  
  def get_result(self):
    #return self.test_django_annotation()
    #self.insert_data()
    #return self.alchemy_query()
    #return self.django_query()
    return self.django_raw_query()
  
  def alchemy_query(self):
    result = TripInterval.sa.query().all()
    
    
    
    return result
    
    
  def django_query(self): # this shit doesn't work!!
    id_row = Window(RowNumber(), order_by=F('id').asc())
    time_row = Window(RowNumber(), partition_by=F('time'), order_by=F('id').asc())
    
    queryset = TripInterval.objects.annotate(
      time_grp=id_row - time_row
    ).values(
      'time', 'time_grp'
    ).annotate(
      start_id=Min('id'), end_id=Max('id')
    ).order_by(
     'start_id'
    ).values(
      'time', 'start_id', 'end_id'
    )
    
    return [item for item in queryset.iterator()]
  
  def django_raw_query(self):
    with connection.cursor() as c:
      print('connection.vendor =', connection.vendor)
      c.execute(
        """
        SELECT "subquery"."time" AS "time",
            MIN("subquery"."id") AS "start_id",
            MAX("subquery"."id") AS "end_id"
        FROM (
          SELECT
            "request_tripinterval"."id",
            "request_tripinterval"."time",
            (
              ROW_NUMBER() OVER (ORDER BY "request_tripinterval"."id" ASC)
              -
              ROW_NUMBER() OVER (PARTITION BY "request_tripinterval"."time" ORDER BY "request_tripinterval"."id" ASC)
            ) AS "time_grp"
          FROM
            "request_tripinterval"
        ) as subquery
        GROUP BY "time", "time_grp"
        ORDER BY "start_id" ASC
        """
      )
      return c.fetchall()
  
  def test_django_annotation(self):
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