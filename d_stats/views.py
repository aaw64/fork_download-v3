# Create your views here.
from django.http import Http404
from django.http import HttpResponse , HttpRequest



def download_file(request):
    from .helpers import FileRegistry   
    file_registry = FileRegistry()
    f = file_registry.get_file(request)
    if f.is_valid():
        return f.send_file()
    else:
        raise Http404


