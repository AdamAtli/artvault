from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Bid
from artworks.models import Artwork
from decimal import Decimal
@login_required
def place_bid(request, artwork_id):
    if request.method == "POST":
        artwork = get_object_or_404(Artwork, pk=artwork_id)
        highest_bid = artwork.bids.order_by('-amount').first()
        new_amount = Decimal(request.POST.get('amount'))
        expiration_date = request.POST.get('expiration_date') or None

        bid = Bid(buyer=request.user.buyer, artwork=artwork, amount=new_amount, expiration_date=expiration_date)
        try:
            bid.full_clean()
            bid.save()
            messages.success(request, "Bid placed successfully")
        except ValidationError as e:
            messages.error(request, e.messages)
            
    return redirect("artworks-detail", id=artwork_id)
