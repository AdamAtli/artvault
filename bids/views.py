from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Bid, BidContingency
from artworks.models import Artwork
from decimal import Decimal
from .utils import expire_old_bids
from .forms import SellerContingencyForm, BuyerContingencyResponseForm
from django.utils import timezone

@login_required
def place_bid(request, artwork_id):
    expire_old_bids()
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
    expire_old_bids()
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
    expire_old_bids()
    bid = get_object_or_404(Bid, pk=bid_id)

    if bid.artwork.seller.user != request.user:
        messages.error(request, "You are not allowed to update this bid")
        return redirect("artworks-detail", id=bid.artwork.id)

    if bid.status == "expired":
        messages.error(request, "This bid is expired and cannot be updated")
        return redirect("artworks-detail", id=bid.artwork.id)

    if status not in ["pending","accepted", "rejected", "contingent"]:
        messages.error(request, "Invalid bid status")
        return redirect("artworks-detail", id=bid.artwork.id)

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

@login_required
def create_contingency(request, bid_id):
    expire_old_bids()
    bid = get_object_or_404(Bid, pk=bid_id)

    if bid.artwork.seller.user != request.user:
        messages.error(request, "You are not allowed to create requirements for this bid")
        return redirect("artworks-detail", id=bid.artwork.id)

    if bid.status == "expired":
        messages.error(request, "This bid is expired")
        return redirect("artworks-detail", id=bid.artwork.id)

    if request.method == "POST":
        form = SellerContingencyForm(request.POST)

        if form.is_valid():
            contingency, created = BidContingency.objects.get_or_create(bid=bid)
            contingency.seller_message = form.cleaned_data["seller_message"]
            contingency.buyer_response = ""
            contingency.buyer_message = ""
            contingency.responded_at = None
            contingency.save()

            bid.status = "contingent"
            bid.save()

            messages.success(request, "Contingency requirements sent to buyer")
            return redirect("artworks-detail", id=bid.artwork.id)
    else:
        form = SellerContingencyForm()

    return render(request, "bid/create_contingency.html", {
        "bid": bid,
        "form": form,
    })

@login_required
def contingency_detail(request, bid_id):
    expire_old_bids()

    bid = get_object_or_404(Bid, pk=bid_id)
    contingency = get_object_or_404(BidContingency, bid=bid)

    is_seller = bid.artwork.seller.user == request.user
    is_buyer = bid.buyer.user == request.user

    if not is_seller and not is_buyer:
        messages.error(request, "You are not allowed to view this contingency")
        return redirect("artworks-detail", id=bid.artwork.id)

    if is_buyer and request.method == "POST":
        form = BuyerContingencyResponseForm(request.POST, instance=contingency)

        if form.is_valid():
            response = form.save(commit=False)
            response.responded_at = timezone.now()
            response.save()

            messages.success(request, "Your response was sent to seller")
            return redirect("contingency-detail", bid_id=bid.id)

    else:
        form = BuyerContingencyResponseForm(instance=contingency)

    return render(request, "bid/contingency_detail.html", {
        "bid": bid,
        "contingency": contingency,
        "form": form,
        "is_seller": is_seller,
        "is_buyer": is_buyer,
    })

