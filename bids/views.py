from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Bid
from artworks.models import Artwork
from decimal import Decimal
@login_required
def place_bid(request, artwork_id):
    if request.method == "POST":
        artwork = get_object_or_404(Artwork, pk=artwork_id)

        if not artwork.is_available:
            messages.error(request, "Bidding is closed for this artwork.")
            return redirect("artworks-detail", id=artwork_id)


        new_amount = Decimal(request.POST.get('amount'))
        expiration_date = request.POST.get('expiration_date') or None

        bid = Bid.objects.filter(buyer=request.user.buyer, artwork=artwork, status="pending").first()

        if bid:
            if new_amount < bid.amount:
                messages.error(request, f"Your current bid is ${bid.amount}. New bid must be higher")
                return redirect("artworks-detail", id=artwork_id)
            bid.amount = new_amount
            bid.expiration_date = expiration_date
        else:
            bid  = Bid(
                buyer=request.user.buyer,
                artwork=artwork,
                amount=new_amount,
                expiration_date=expiration_date,
            )

        try:
            bid.full_clean()
            bid.save()
            messages.success(request, "Bid placed successfully")
        except ValidationError as e:
            messages.error(request, e.messages)
            
    return redirect("artworks-detail", id=artwork_id)

@login_required
def delete_bid(request, bid_id):
    bid = get_object_or_404(
        Bid,
        pk=bid_id,
        buyer=request.user.buyer,
    )
    if request.method == "POST":
        bid.delete()
        messages.success(request, "Bid deleted successfully")
    return redirect("my-bids")

@login_required
def update_bid_status(request, bid_id, status):
    bid = get_object_or_404(Bid, pk=bid_id)

    if bid.artwork.seller.user != request.user:
        messages.error(request, "You are not allowed to update this bid")
        return redirect("artworks-detail", id=bid.artwork.id)

    if status not in ["pending","accepted", "rejected", "contingent"]:
        messages.error(request, "Invalid bid status")

    if status in ["accepted", "contingent"]:
        existing_bid = bid.artwork.bids.filter(
            status__in=["accepted", "contingent"]
        ).exclude(pk=bid.pk).first()

        if existing_bid:
            messages.error(request, "Bid already accepted or is contingent")
            return redirect("artworks-detail", id=bid.artwork.id)

    bid.status = status
    bid.save()

    messages.success(request, f"Bid marked as {bid.get_status_display()}.")
    return redirect("artworks-detail", id=bid.artwork.id)