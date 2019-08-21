from django import forms

class Actions:
  CREATE = 'create'
  TEST = 'test'

action_choices = (
  (Actions.CREATE, 'create'),
  (Actions.TEST, 'test'),
)

class RequestForm(forms.Form):
  action = forms.ChoiceField(choices=action_choices)
  username = forms.CharField()
  offset = forms.IntegerField()
  limit = forms.IntegerField()
  vehicle_name = forms.CharField()
  vehicle_path = forms.FloatField()
  vehicle_time = forms.FloatField()
