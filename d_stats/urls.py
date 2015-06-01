from django.conf.urls.defaults import *   
from django.views.generic import TemplateView 
import views as download_stats_views

urlpatterns = patterns(' ',
 url(r'^/user/download/get$', 'download_stats_views.download_file'),
)
