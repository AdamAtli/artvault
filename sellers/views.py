from django.shortcuts import render, get_object_or_404

from sellers.models import Seller
def index(request):
    sellers = Seller.objects.all()

    return render(request, "seller/sellers.html", {
        "sellers": sellers
    })

def get_seller_by_id(request, id):
    seller = get_object_or_404(Seller, pk=id)

    return render(request, "seller/seller_details.html", {
        "seller": seller
    })
