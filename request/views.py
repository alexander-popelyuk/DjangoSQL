from django.views.generic import FormView
from django.core.exceptions import ObjectDoesNotExist
from .forms import RequestForm

class RequestView(FormView):
  template_name = "request.html"
  form_class = RequestForm
  success_url = "/"
  
  def get_initial(self):
    return {
      'offset': 0,
      'limit': 100,
    }
  
  def form_valid(self, form):
    self.handle_request(form.cleaned_data)
    return super().form_invalid(form)
  
  def handle_request(self, params):
    pass