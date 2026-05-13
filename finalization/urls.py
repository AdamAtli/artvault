from django.urls import path
from . import views

urlpatterns = [
    path('<int:bid_id>/contact/', views.finalize_contact, name='finalize-contact'),
    path('<int:bid_id>/payment/', views.finalize_payment, name='finalize-payment'),
    path("<int:bid_id>/review/", views.finalize_review, name='finalize-review'),
    path("<int:bid_id>/confirmation", views.finalize_confirmation, name='finalize-confirmation'),
]