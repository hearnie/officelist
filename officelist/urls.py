from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from views import *
#from views import gaterange_result
#from views import search_form
#from views import result
#from views import caprange_result
#from views import search_caprange


urlpatterns = patterns('',

    url(r'^$', search_gaterange),
    url(r'^search_caprange/$', search_caprange),
    url(r'^caprange_result/$', caprange_result),
    url(r'^search_gaterange/$', search_gaterange),
    url(r'^gaterange_result/$', gaterange_result),
    url(r'^igb/$', igb),
    #url(r'^caprange_result_addressbar/(\w{1,15})$', caprange_result_addressbar),
    #url(r'^officelist/', include('officelist.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)

