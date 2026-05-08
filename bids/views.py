from django.shortcuts import render, get_object_or_404, redirect
from pyexpat.errors import messages

from .models import Bid
from artworks.models import Artwork

def place_bid(request, artwork_id):
    if request.method == "POST":
        artwork = get_object_or_404(Artwork, pk=artwork_id)
        highest_bid = artwork.bids.order_by('-amount').first()
        new_amount = Decimal(request.POST.get('amount'))

        if highest_bid and new_amount <= highest_bid.amount:
            messages.error(request, f"Your bid must be higher than {highest_bid.amount}")
        else:
            Bid.objects.create(artwork=artwork, buyer=request.user.buyer, amount=new_amount)
            messages.success(request, f"Your bid has been placed successfully")
    return redirect("artworks-detail", artwork_id)
