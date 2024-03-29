import datetime
from time import mktime
import hashlib

from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

import goBuySocial.settings

from paypal.standard.ipn.signals import payment_was_successful, payment_was_flagged

def upload_dir(instance, filename):
    return "deals/%s/%d/%d/%s" % (instance.campus.shortname, datetime.datetime.now().year, datetime.datetime.now().month, filename)
    
class Deal(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to=upload_dir)
    image_caption = models.TextField()
    company = models.CharField(max_length=50)
    company_url = models.CharField(max_length=80)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    full_price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField()
    disclaimer = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_open = models.DateTimeField(auto_now_add=True)
    date_expires = models.DateTimeField()
    campus = models.ForeignKey('Campus')
    hash = models.CharField(max_length=40, blank=True, null=True)
    added_by = models.ForeignKey(User)
    
    def expired(self):
        return self.seconds_remaining() > 0
        
    def seconds_remaining(self):
        return (self.date_expires - datatime.datetime.now()).seconds
    
    def expires_in_ms(self):
        return 1000 * mktime(self.date_expires.timetuple())
    
    def savings(self):  
        return self.full_price - self.price
    
    def save(self, *args, **kwargs):
        super(Deal, self).save(*args, **kwargs)
        if not self.hash:
            m = hashlib.md5()
            m.update(str(self.pk))
            m.update(goBuySocial.settings.SECRET_KEY)
            self.hash = m.hexdigest()
        super(Deal, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return "%s: %s" % (self.title, str(self.date_expires))
    

class Campus(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=60)
    shortname = models.CharField(max_length=15)
    background_image = models.ImageField(upload_to="campus")
    thumbnail_image = models.ImageField(upload_to="campus")
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    class Meta:
        verbose_name_plural = "campuses"
    
    def __unicode__(self):
        return "%s" % (self.name)

class Purchase(models.Model):
    deal = models.ForeignKey(Deal)
    date_bought = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=80)
    purchase_complete = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s bought %s on %s" % (self.email, str(self.deal), str(self.date_bought))
    
class Saved(models.Model):
    value = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    
    def digits(self):
        str_value = str(self.value)
        decimal_loc = str_value.find(".") if str_value.find(".") != -1 else len(str_value)
        str_value = str_value[0:decimal_loc]
        digits = []
        for i, d in enumerate(str_value):
            digits.append(d)
        return digits
    
    def __unicode__(self):
        return "%s: %s" % (str(self.date), str(self.value))

def successful_payment(sender, **kwargs):
    ipn_obj = sender
    deal_pk = ipn_obj.custom
    deal = Deal.objects.get(pk=deal_pk)
    payer_email = ipn_obj.payer_email
    purchase = Purchase(deal=deal, first_name=ipn_obj.first_name,
                        last_name=ipn_obj.last_name,
                        email=payer_email,
                        purchase_complete=True)
    purchase.save()

def flagged_payment(sender, **kwargs):
    ipn_obj = sender
    deal_pk = ipn_obj.custom
    deal = Deal.objects.get(pk=deal_pk)
    payer_email = ipn_obj.payer_email
    purchase = Purchase(deal=deal, first_name=ipn_obj.first_name,
                        last_name=ipn_obj.last_name,
                        email=payer_email,
                        purchase_complete=False)
    purchase.save()
    
payment_was_successful.connect(successful_payment)
payment_was_flagged.connect(flagged_payment)
