from django.shortcuts import render, get_object_or_404


from .models import Buyer
from artworks.models import Artwork

def buyer_detail(request, pk):

    buyer = get_object_or_404(Buyer, pk=pk)
    bids = buyer.bids.all()
    artworks = Artwork.objects.filter(bids__buyer=buyer).distinct()


    return render(request, "buyer/buyer_details.html", {
        "buyer": buyer,
        "bids": bids,
        "artworks": artworks

    })
