import httplib2, urllib

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from deals.models import Campus, Deal, Saved
from goBuySocial import settings
from paypal.standard.forms import PayPalPaymentsForm


def home(request, campus_shortname=None):
    campus = campus_from_shortname(campus_shortname)
    campuses = Campus.objects.all()
    saved = Saved.objects.all().order_by("-date")
    if saved.count():
        saved = saved[0]
    else:
        saved = Saved(value=00.0)
            
    deals = Deal.objects.filter(campus=campus).order_by("-date_expires")
    if deals.count() >= 1:
        deal = deals[0]
        recent_deals = deals[1:3]
    else:
        deal = None
        recent_deals = None
    if deal:
        paypal_dict = {
            "business": "seller_1333326312_biz@taylorsavage.com",
            "amount": deal.price,
            "item_name": deal.title,
            "custom": deal.pk,
            "notify_url": "http://www.gobuysocial.com/ipn_handler/",
            "return_url": "http://www.gobuysocial.com/purchased/",
            "cancel_return": "http://www.gobuysocial.com",
        }
    else:
        paypal_dict = None
    
    form = PayPalPaymentsForm(initial=paypal_dict)
    
    return render_to_response('gb_home.html',
                            {'campus':campus,
                            'campuses':campuses,
                            'deal':deal,
                            'deal_form':form,
                            'saved': saved,
                            'starting_digit': 6 - len(saved.digits()),
                            'recent_deals':recent_deals},
                            context_instance=RequestContext(request, {'BASE_URL': settings.BASE_URL,}))

def deal(request, campus_shortname, deal_id):
    return HttpResponse("Hi")
    
def buy(request, campus_shortname, deal_id):
    deal = get_object_or_404(Deal, pk=deal_id)
    campus = campus_from_shortname(campus_shortname)
    
    paypal_dict = {
        "business": "seller_1333326312_biz@taylorsavage.com",
        "amount": deal.price,
        "item_name": deal.title,
        "notify_url": "http://www.gobuysocial.com/ipn_handler/",
        "return_url": "http://www.gobuysocial.com/purchased/",
        "cancel_return": "http://www.gobuysocial.com",
        "custom": deal.pk,
    }
    
    form = PayPalPaymentsForm(initial=paypal_dict)
    
    
    return render_to_response('buy.html',
                            {'deal': deal, 
                            'campus':campus,
                            'form':form},
                            context_instance=RequestContext(request, {'BASE_URL': settings.BASE_URL,}))

def about(request):
    campuses = Campus.objects.all()
    
    return render_to_response('about.html',
                            {'campuses':campuses,},
                            context_instance=RequestContext(request, {'BASE_URL': settings.BASE_URL, }))

def purchased(request):
    return HttpResponse("hello")
    
def buyers(request, deal_hash):
    return HttpResponse("hi")

def ipn_handler(request):
    data = request.POST
    url = 'https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_notify-validate&'
    u = urllib.urlopen(url)
    response = u.read()
    return HttpResponse("Done")

def campus_from_shortname(campus_shortname):
    if campus_shortname == None:
        campus = Campus.objects.get(name='Stanford')
    else:   
        campus = None
        campus = Campus.objects.get(shortname=campus_shortname)
    
    return campus
