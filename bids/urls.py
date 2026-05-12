from django.urls import path
from . import views


urlpatterns = [
    path('artworks/<int:artwork_id>/bid', views.place_bid, name='place_bid'),
    path('bids/<int:bid_id>/delete', views.delete_bid, name='delete-bid'),
    path("bids/<int:bid_id>/<str:status>/", views.update_bid_status, name="update-bid-status"),
]
