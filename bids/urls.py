from django.urls import path
from . import views


urlpatterns = [
    path('artworks/<int:artwork_id>/bid', views.place_bid, name='place_bid'),
]
