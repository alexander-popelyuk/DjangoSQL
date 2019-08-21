from django import forms

action_choices = (
  ('create', 'create'),
  ('delete', 'delete'),
  ('update', 'update'),
)

class RequestForm(forms.Form):
  action = forms.ChoiceField(choices=action_choices)
  username = forms.CharField()
  offset = forms.IntegerField()
  limit = forms.IntegerField()
