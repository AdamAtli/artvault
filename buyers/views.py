from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BuyerProfileForm

from .models import Buyer

def buyer_detail(request, pk):

    buyer = get_object_or_404(Buyer, pk=pk)
    bids = buyer.bids.select_related('artwork', 'artwork__seller').order_by(
        "artwork_id",
        "-timestamp",
    )
    latest_bids = []
    seen_artworks = set()

    for bid in bids:
        if bid.artwork_id not in seen_artworks:
            latest_bids.append(bid)
            seen_artworks.add(bid.artwork_id)

    return render(request, "buyer/buyer_details.html", {
        "buyer": buyer,
        "bids": latest_bids,


    })

@login_required
def edit_buyer_profile(request):
    buyer = request.user.buyer

    if request.method == "POST":
        form = BuyerProfileForm(request.POST, request.FILES, instance=buyer)

        if form.is_valid():
            form.save()
            messages.success(request, "Your profile was successfully updated!")

            return redirect("buyer-detail", pk=buyer.id)

    else:
        form = BuyerProfileForm(instance=buyer)

    return render(request, "buyer/edit_buyer_profile.html", {
        "form": form,
        "buyer": buyer,
    })