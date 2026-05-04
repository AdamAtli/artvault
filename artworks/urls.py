from django.urls import path
from . import views
urlpatterns = [
    # http://localhost:8000
    path('', views.index, name='artworks-index'),
    # http://localhost:8000/<int>
    path('<int:id>', views.get_art_by_id, name='artworks-detail'),
]