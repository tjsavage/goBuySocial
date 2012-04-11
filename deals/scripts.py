from models import Saved, Purchase, Deal

def update_saved():
    total_saved = 0
    for purchase in Purchase.objects.filter(purchase_complete=True):
        deal = purchase.deal
        total_saved += deal.savings()
        
    s = Saved(value=total_saved)
    s.save()
