from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)), 
    (r'^cheap/gettree/', 'cheapest_apple.cheapestapple.views.getTree'),
    (r'^cheap/getproducts/', 'cheapest_apple.cheapestapple.views.getProducts'),
    (r'^cheap/getprices/', 'cheapest_apple.cheapestapple.views.getPrices'),
    (r'^cheap/', 'cheapest_apple.cheapestapple.views.index'),   
    (r'^sara/', 'cheapest_apple.cheapestapple.views.sara'),
    (r'^robots\.txt$', direct_to_template,
     {'template': 'robots.txt', 'mimetype': 'text/plain'}),
    (r'^(?P<type>\w+)/(?P<page_id>\d+)/', 'cheapest_apple.cheapestapple.views.noJSindex'),
    (r'^$', 'cheapest_apple.cheapestapple.views.noJSindex', {'type': 'box', 'page_id': '1'}),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/home/vkozyrev/webapps/cheapest_apple/cheapest_apple/site_media'}),               
)

