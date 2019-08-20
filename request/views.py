from django.views.generic import TemplateView
from django.http.response import HttpResponse, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist

class Forbidden(Exception):
  pass

class BadRequest(Exception):
  pass

class RequestView(TemplateView):
  def get(self, request, *args, **kwargs):
    response = "Hello world!"
    params = ''
    for param_name, param_value in request.GET.items():
      if params:
        params += ', '
      params += '%s=%s' % (param_name, param_value)
    response += "<br/>Query parameters: " + params
    response += "<br/>" + self.handle_session(request)
    
    return HttpResponse(response)
  
  def handle_session(self, request):
    action = request.GET.get('action', 'list')
    username = request.GET.get('limit', 100)
    

    self.print_requests(request)
    return HttpResponseForbidden()
    
  def print_requests(self, request):
    offset = request.GET.get('offset', 0)
    limit = request.GET.get('limit', 100)
    pass

  