
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Max, Min
from artworks.forms.artwork_create_form import ArtworkCreateForm, ImageCreateForm
from artworks.models import Artwork, Image, ArtworkFilter
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q


def get_filtered_artworks(request, queryset=None):
    if queryset is None:
        queryset = Artwork.objects.select_related("seller").all()

    f = ArtworkFilter(request.GET, queryset=queryset)
    artworks = f.qs

    if request.GET.get("max_price"):
        artworks = artworks.filter(starting_bid_price__lte=request.GET["max_price"])

    if request.GET.get("max_year"):
        artworks = artworks.filter(year_of_creation__lte=request.GET["max_year"])

    for artwork in artworks:
        artwork.user_bid = None

        if request.user.is_authenticated and hasattr(request.user, "buyer"):
            artwork.user_bid = artwork.bids.filter(buyer=request.user.buyer).first()

    max_price = Artwork.objects.aggregate(Max("starting_bid_price"))["starting_bid_price__max"] or 0
    min_year = Artwork.objects.aggregate(Min("year_of_creation"))["year_of_creation__min"] or 1600
    max_year = Artwork.objects.aggregate(Max("year_of_creation"))["year_of_creation__max"] or 2026

    return {
        "filter": f,
        "artworks": artworks,
        "max_price": max_price,
        "min_year": min_year,
        "max_year": max_year,
    }

def index(request):
    context = get_filtered_artworks(request)

    artworks = context["artworks"]

    search = request.GET.get("search")

    if search:
        artworks = artworks.filter(
            Q(title__icontains=search) |
            Q(seller__user__username__icontains=search)
        )

    paginator = Paginator(artworks, 9)

    page_number = request.GET.get("page")

    context["artworks"] = paginator.get_page(page_number)

    return render(request, "artwork/artworks.html", context)

def get_art_by_id(request, id):
    artwork = get_object_or_404(Artwork, pk=id)

    user_bid = None

    if request.user.is_authenticated and hasattr(request.user, "buyer"):
        user_bid = artwork.bids.filter(buyer=request.user.buyer).first()

    artwork.user_bid = user_bid
    
    return render(request, "artwork/artwork_details.html", {
        "artwork": artwork,
        "user_bid": user_bid
    })

@login_required
def create_artwork(request):

    if not request.user.seller.is_approved:
        messages.error(request, "Your seller account has not been approved yet")
        return redirect("seller-detail", id=request.user.seller.id)

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


