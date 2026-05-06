from django.http import HttpResponse
from django.shortcuts import render

from data import sellers
def index(request):
    # TODO: Retrieve data from database
    # TODO: Populate a template with data coming from database
    return render(request, "seller/sellers.html", {
        "sellers": sellers
    })

def get_seller_by_id(request, id):
    # TODO: Retrieve data from database
    # TODO: Populate a template with data coming from database
    seller = [x for x in sellers if x["id"] == id][0]
    return render(request, "seller/seller_details.html", {
        "seller": seller
    })
