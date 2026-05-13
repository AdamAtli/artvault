from artworks.models import Medium, Style

def artwork_navigation(request):

    return {
        "nav_mediums": Medium.objects.all(),
        "nav_styles": Style.objects.all(),
    }