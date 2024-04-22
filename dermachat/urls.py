from django.urls import path
from . import views

urlpatterns = [
    path("dermachat", views.dermachat_view, name='dermachat'),  # Use dermachat_view for the combined functionality
]
