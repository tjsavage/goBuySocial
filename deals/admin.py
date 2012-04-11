from django.contrib import admin

from deals.models import Deal, Campus, Purchase, Saved

admin.site.register(Deal)
admin.site.register(Campus)
admin.site.register(Purchase)
admin.site.register(Saved)