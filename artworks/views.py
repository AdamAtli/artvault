from django.http import HttpResponse
from django.shortcuts import render

from data import artworks


def index(request):
    # TODO: Retrieve data from database
    # TODO: Populate a template with data coming from database
    return render(request, "artwork/artworks.html", {
        "artworks": artworks
    })

def get_art_by_id(request, id):
    # TODO: Retrieve data from database
    # TODO: Populate a template with data coming from database
    artwork = [x for x in artworks if x["id"] == id][0]
    return render(request, "artwork/artwork_details.html", {
        "artwork": artwork
    })
