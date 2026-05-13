from django.urls import path
from . import views

urlpatterns = [
    # http://localhost:8000
    path('', views.index, name='artworks-index'),
    # http://localhost:8000/<int>
    path('<int:id>', views.get_art_by_id, name='artworks-detail'),

    path('create_artwork', views.create_artwork, name='create-artwork'),

    path("about/", views.about, name="about"),

    path( "contact/", views.contact_us, name="contact-us"),
]