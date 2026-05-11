from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.buyer_detail, name='buyer-detail'),
    path('edit/', views.edit_buyer_profile, name='edit-buyer-profile'),
]