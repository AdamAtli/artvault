from django.urls import path
from . import views

urlpatterns = [
    # http://localhost:8000
    path('', views.index, name='seller-index'),
    # http://localhost:8000/<int>
    path('edit/', views.edit_seller_profile, name='edit-seller-profile'),
    path('<int:id>', views.get_seller_by_id, name='seller-detail'),

]