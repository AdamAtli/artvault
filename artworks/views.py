from django.shortcuts import render, get_object_or_404

from artworks.models import Artwork



def index(request):
    artworks = Artwork.objects.all()

    return render(request, "artwork/artworks.html", {
        "artworks": artworks
    })

def get_art_by_id(request, id):
    artwork = get_object_or_404(Artwork, pk=id)

    return render(request, "artwork/artwork_details.html", {
        "artwork": artwork
    })
