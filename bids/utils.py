from django.utils import timezone
from .models import Bid

def expire_old_bids():
    today = timezone.localdate()

    return Bid.objects.filter(
        status="pending",
        expiration_date__isnull=False,
        expiration_date__lte=today,
    ).update(status="expired")