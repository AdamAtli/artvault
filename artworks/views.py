from django.http import HttpResponse
from django.shortcuts import render

from data import artworks, sellers


def index(request):
    # TODO: Retrieve data from database
    # TODO: Populate a template with data coming from database
    for artwork in artworks:
        seller = [x for x in sellers if x["id"] == artwork["seller_id"]][0]
        
        artwork["seller_name"] = seller["name"]
        artwork["seller_logo"] = seller["logo"]

    return render(request, "artwork/artworks.html", {
        "artworks": artworks
    })

def get_art_by_id(request, id):
    # TODO: Retrieve data from database
    # TODO: Populate a template with data coming from database
    artwork = [x for x in artworks if x["id"] == int(id)][0]

    seller = [x for x in sellers if x["id"] == artwork["seller_id"]][0]
    artwork["seller_name"] = seller["name"]
    artwork["seller_logo"] = seller["logo"]

    return render(request, "artwork/artwork_details.html", {
        "artwork": artwork
    })
