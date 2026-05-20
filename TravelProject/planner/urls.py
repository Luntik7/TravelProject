from django.contrib import admin
from django.urls import path
from .routers import travel_router
from planner import *
from .views import *


urlpatterns = [
    path('artworks/', ArtSearchAPIView.as_view()),
]
