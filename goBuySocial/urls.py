from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'deals.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/$', 'deals.views.about'),
    url(r'^purchased/$', 'deals.views.purchased'),
    url(r'^ipn_handler/$', include('paypal.standard.ipn.urls')),
    url(r'^(?P<campus_shortname>\w+)/', include('deals.urls')),
    url(r'^buyers/(?P<deal_hash>\w+)/', 'deals.views.buyers'),
    

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    
)

urlpatterns += staticfiles_urlpatterns()