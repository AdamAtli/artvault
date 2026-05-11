from django.db.models import Min, Max
from django.shortcuts import render, get_object_or_404, redirect

from artworks.forms.artwork_create_form import ArtworkCreateForm, ImageCreateForm
from artworks.models import Artwork, Image
from django.contrib.auth.decorators import login_required

def filter_artworks(request, artworks):

    medium = request.GET.get("medium")
    style = request.GET.get("style")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    size = request.GET.get("size")
    year_of_creation = request.GET.get("year_of_creation")
    edition = request.GET.get("edition")

    if medium:
        artworks = artworks.filter(medium__iexact=medium)
    if style:
        artworks = artworks.filter(style__iexact=style)
    if min_price:
        artworks = artworks.filter(starting_bid_price__gte=min_price)
    if max_price:
        artworks = artworks.filter(starting_bid_price__lte=max_price)
    if size == "small":
        artworks = artworks.filter(width_cm__lte=30, height_cm__lte=30)
    elif size == "medium":
        artworks = artworks.filter(width_cm__lte=100, height_cm__lte=100)
    elif size == "large":
        artworks = artworks.filter(width_cm__gt=100)
    if year_of_creation:
        artworks = artworks.filter(year_of_creation=year_of_creation)
    if edition:
        artworks = artworks.filter(edition__iexact=edition)

    return artworks


def index(request):
    artworks = Artwork.objects.all()
    artworks = filter_artworks(request, artworks)
    prices = Artwork.objects.aggregate(
        min_price=Min("starting_bid_price"),
        max_price=Max("starting_bid_price"),
    )

    return render(request, "artwork/artworks.html", {
        "artworks": artworks,
        "mediums": Artwork.objects.values_list("medium", flat=True).distinct(),
        "styles": Artwork.objects.values_list("style", flat=True).distinct(),
        "min_price": prices["min_price"],
        "max_price": prices["max_price"],
        "year_of_creation": Artwork.objects.values_list("year_of_creation", flat=True).distinct().order_by("year_of_creation"),
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


