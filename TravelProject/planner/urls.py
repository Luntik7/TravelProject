from django.contrib import admin
from django.urls import path
from planner import *
from .views import *


urlpatterns = [
    path('artworks/', ArtSearchAPIView.as_view()),
    path('travels/', TravelListCreateAPIView.as_view()),
    path('travels/<int:pk>/', TravelDetailAPIView.as_view()),
    path('travels/<int:pk>/places/', PlaceListCreateAPIView.as_view()),
    path('travels/<int:travel_pk>/places/<int:place_pk>/', PlaceRetrieveUpdateAPIView.as_view())
]
