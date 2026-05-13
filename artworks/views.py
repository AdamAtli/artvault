
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Max, Min, Q
from artworks.forms.artwork_create_form import ArtworkCreateForm, ImageCreateForm
from artworks.models import Artwork, Image, Medium, Style
from .filters import ArtworkFilter
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models.functions import Coalesce
from bids.utils import expire_old_bids


def get_filtered_artworks(request, queryset=None):
    expire_old_bids()
    if queryset is None:
        queryset = Artwork.objects.select_related("seller").all()

    queryset = queryset.annotate(
        current_price=Coalesce(
            Max("bids__amount", filter=~Q(bids__status__in=["expired", "rejected"])),
            "starting_bid_price"
        )
    )

    f = ArtworkFilter(request.GET, queryset=queryset)
    artworks = f.qs

    if request.GET.get("max_price"):
        artworks = artworks.filter(current_price__lte=request.GET["max_price"])

    if request.GET.get("max_year"):
        artworks = artworks.filter(year_of_creation__lte=request.GET["max_year"])

    availability = request.GET.get("availability")

    if availability == "available":
        artworks = artworks.exclude(
            is_sold=True
        ).exclude(
            bids__status__in=["accepted", "contingent", "finalized"]
        )

    elif availability == "sold":
        artworks = artworks.filter(
            Q(is_sold=True) |
            Q(bids__status__in=["accepted", "contingent", "finalized"])
        )

    artworks = artworks.distinct()

    for artwork in artworks:
        artwork.user_bid = None

        if request.user.is_authenticated and hasattr(request.user, "buyer"):
            artwork.user_bid = artwork.bids.filter(buyer=request.user.buyer).first()

    max_price = queryset.aggregate(Max("current_price"))["current_price__max"] or 0
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
    expire_old_bids()
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
            form.save_m2m()

            new_medium = form.cleaned_data.get("new_medium")

            if new_medium:
                medium, created = Medium.objects.get_or_create(
                    name=new_medium.strip().title()
                )

                artwork.mediums.add(medium)

            new_style = form.cleaned_data.get("new_style")

            if new_style:
                style, created = Style.objects.get_or_create(
                    name=new_style.strip().title()
                )
                artwork.style = style

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

def about(request):
    return render(request, "user/about.html")

def contact_us(request):
    return render(request, "user/contact_us.html")




