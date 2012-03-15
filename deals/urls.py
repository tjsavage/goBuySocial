from django.conf.urls import patterns, include, url

urlpatterns = patterns('deals.views',
    # Examples:
    url(r'^$', 'home'),
    url(r'^(?P<deal_id>\d+)/buy/$', 'buy'),
    url(r'^(?P<deal_id>\d+)/$', 'deal'),
    

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
