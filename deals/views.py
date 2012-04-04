import httplib2, urllib

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext

from deals.models import Campus, Deal
from goBuySocial import settings

def home(request, campus_shortname=None):
    campus = campus_from_shortname(campus_shortname)
    campuses = Campus.objects.all()
    
    deals = Deal.objects.filter(campus=campus).order_by("-date_expires")
    if deals.count() >= 1:
        deal = deals[0]
        recent_deals = deals[1:3]
    else:
        deal = None
        recent_deals = None
    
    return render_to_response('home.html',
                            {'campus':campus,
                            'campuses':campuses,
                            'deal':deal,
                            'recent_deals':recent_deals},
                            context_instance=RequestContext(request, {'BASE_URL': settings.BASE_URL,}))

def deal(request, campus_shortname, deal_id):
    return HttpResponse("Hi")
    
def buy(request, campus_shortname, deal_id):
    deal = get_object_or_404(Deal, pk=deal_id)
    campus = campus_from_shortname(campus_shortname)
    
    return render_to_response('buy.html',
                            {'deal': deal, 
                            'campus':campus,},
                            context_instance=RequestContext(request, {'BASE_URL': settings.BASE_URL,}))

def about(request):
    campuses = Campus.objects.all()
    
    return render_to_response('about.html',
                            {'campuses':campuses,},
                            context_instance=RequestContext(request, {'BASE_URL': settings.BASE_URL, }))

def purchased(request):
    return HttpResponse("hello")

def ipn_handler(request):
    data = request.POST
    print data
    url = 'https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_notify-validate&'
    print url
    u = urllib.urlopen(url)
    response = u.read()
    print response
    return HttpResponse("Done")

def campus_from_shortname(campus_shortname):
    if campus_shortname == None:
        campus = Campus.objects.get(name='Stanford')
    else:   
        campus = None
        campus = Campus.objects.get(shortname=campus_shortname)
    
    return campus
    