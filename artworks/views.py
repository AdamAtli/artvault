from django.shortcuts import render, get_object_or_404, redirect

from artworks.forms.artwork_create_form import ArtworkCreateForm, ImageCreateForm
from artworks.models import Artwork, Image
from django.contrib.auth.decorators import login_required



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

@login_required
def create_artwork(request):
    if request.method == "POST":
        form = ArtworkCreateForm(request.POST)
        image_form = ImageCreateForm(request.POST, request.FILES)

        if form.is_valid() and image_form.is_valid():
            artwork = form.save(commit=False)
            artwork.seller = request.user.seller
            artwork.save()

            for uploaded_image in request.FILES.getlist("image"):
                Image.objects.create(artwork=artwork, image=uploaded_image)

            return redirect("artworks-detail", id=artwork.id)

    else:
        form = ArtworkCreateForm()
        image_form = ImageCreateForm()

    return render(request, "artwork/create_artwork.html", {
        "form": form,
        "image_form": image_form
    })