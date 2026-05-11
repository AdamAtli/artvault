from django.shortcuts import render, get_object_or_404
from artworks.models import Artwork
from artworks.views import get_filtered_artworks

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