from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Min, Max
from artworks.views import filter_artworks
from artworks.models import Artwork
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from sellers.forms import SellerProfileForm

from sellers.models import Seller
def index(request):
    sellers = Seller.objects.all()

    return render(request, "seller/sellers.html", {
        "sellers": sellers
    })

def get_seller_by_id(request, id):
    seller = get_object_or_404(Seller, pk=id)
    seller_artworks = Artwork.objects.filter(seller=seller)
    artworks = filter_artworks(request, seller_artworks)

    prices = seller_artworks.aggregate(
        min_price=Min("starting_bid_price"),
        max_price=Max("starting_bid_price"),
    )

    return render(request, "seller/seller_details.html", {
        "seller": seller,
        "artworks": artworks,
        "mediums": seller_artworks.values_list("medium", flat=True).distinct(),
        "styles": seller_artworks.values_list("style", flat=True).distinct(),
        "min_price": prices["min_price"],
        "max_price": prices["max_price"],
        "year_of_creation": seller_artworks.values_list("year_of_creation", flat=True).distinct().order_by("year_of_creation"),
    })

@login_required
def edit_seller_profile(request):
    seller = request.user.seller

    if request.method == "POST":
        form = SellerProfileForm(request.POST, request.FILES, instance=seller)

        if form.is_valid():
            form.save()
            messages.success(request, "Your profile was successfully updated!")
            return redirect("seller-detail", id=seller.id)

    else:
        form = SellerProfileForm(instance=seller)

    return render(request, "seller/edit_seller_profile.html", {
        "form": form,
        "seller": seller,
    })