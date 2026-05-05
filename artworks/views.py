from django.http import HttpResponse
from django.shortcuts import render

import artworks


def index(request):
    # TODO: Retrieve data from database
    # TODO: Populate a template with data coming from database
    return render(request, "artwork/artworks.html", {
        "artworks": artworks
    })
    return HttpResponse(f"Responce from {request.path}")

def get_art_by_id(request, id):
    # TODO: Retrieve data from database
    # TODO: Populate a template with data coming from database
    return HttpResponse(f"Responce from {request.path} with id {id}")
