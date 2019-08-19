from django.views import View
from django.http.response import HttpResponse


class RequestView(View):
  def get(self, request, *args, **kwargs):
    response = "Hello world!"
    params = ''
    for param_name, param_value in request.GET.items():
      if params:
        params += ', '
      params += '%s=%s' % (param_name, param_value)
    response += "<br/>Query parameters: " + params
    
    self.update_session(request)
    self.print_requests(request)
    
    return HttpResponse(response)
  
  def update_session(self, request):
    action = request.GET.get('action', 'list')
    username = request.GET.get('limit', 100)
    
    pass
    
  def print_requests(self, request):
    offset = request.GET.get('offset', 0)
    limit = request.GET.get('limit', 100)
    pass

  