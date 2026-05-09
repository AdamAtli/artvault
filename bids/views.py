from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from pyexpat.errors import messages

from .models import Bid
from artworks.models import Artwork

def place_bid(request, artwork_id):
    if request.method == "POST":
        artwork = get_object_or_404(Artwork, pk=artwork_id)
        highest_bid = artwork.bids.order_by('-amount').first()
        new_amount = Decimal(request.POST.get('amount'))

        bid = Bid(user=request.user.buyer, artwork=artwork, amount=new_amount)
        try:
            bid.full_clean()
            bid.save()
            messages.success(request, "Bid placed successfully")
        except ValidationError as e:
            messages.error(request, e.messages)
            
    return redirect("artworks-detail", artwork_id)
