from django.shortcuts import render, get_object_or_404, redirect
from artworks.models import Artwork
from artworks.views import get_filtered_artworks
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SellerProfileForm

from sellers.models import Seller
def index(request):
    sellers = Seller.objects.all()

    return render(request, "seller/sellers.html", {
        "sellers": sellers
    })

def get_seller_by_id(request, id):
    seller = get_object_or_404(Seller, pk=id)
    queryset = Artwork.objects.filter(seller=seller)
    context = get_filtered_artworks(request, queryset=queryset)
    context['seller'] = seller

    return render(request, "seller/seller_details.html", context)

@login_required
def edit_seller_profile(request):
    seller = request.user.seller

    if request.method == "POST":
        form = SellerProfileForm(request.POST, request.FILES, instance=seller)

        if form.is_valid():
            form.save()
            messages.success(request, "Your profile was successfully updated.")
            return redirect("seller-detail", id=seller.id)

    else:
        form = SellerProfileForm(instance=seller)

    return render(request, "seller/edit_seller_profile.html", {
        "form": form,
        "seller": seller,
    })

@login_required
def my_artworks(request):
    seller = request.user.seller

    queryset = Artwork.objects.filter(seller=seller)
    context = get_filtered_artworks(request, queryset=queryset)
    context['seller'] = seller

    return render(request, "seller/my_artworks.html", context)