from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from .views import TravelViewSet, PlaceViewSet

travel_router = DefaultRouter()
travel_router.register(r"travels", TravelViewSet, basename="travel")


place_router = NestedDefaultRouter(travel_router, r"travels", lookup="travel")#/<parent_prefix>/{lookup(<lookup>_pk )}/<child_prefix>/   
place_router.register(r"places", PlaceViewSet, basename="place")