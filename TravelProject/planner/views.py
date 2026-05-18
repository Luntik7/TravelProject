from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
import requests
from .models import Travel, Place
from .serializers import TravelSerializer, PlaceSerializer
from rest_framework.exceptions import ValidationError


# Create your views here.
class ArtSearchAPIView(APIView):
    def get(self, request):
        page = request.GET.get("page", 1)

        url = "https://api.artic.edu/api/v1/artworks/search"

        response = requests.get(url, timeout=10, params={
            "page": page,
            "limit": 10,
        })

        data = response.json()

        return Response({
            "data": data.get("data"),
            "pagination": data.get("pagination")
        })
    
    
class TravelListCreateAPIView(generics.ListCreateAPIView):
    queryset = Travel.objects.all()
    serializer_class = TravelSerializer


    def perform_create(self, serializer):
        places_data = self.request.data.get("places", [])

        if len(places_data) > 10:
            raise ValidationError({"places": "Maximum 10 places per project."})

        with transaction.atomic():
            travel = serializer.save()

            for item in places_data:
                external_id = item.get("external_id")
                if not external_id: 
                    raise ValidationError({"places": "external_id is required"})

                if travel.places.filter(external_id=external_id).exists():
                    raise ValidationError({"places": f"Place {external_id} already exists in this project"})
                
                response = requests.get(f"https://api.artic.edu/api/v1/artworks/{external_id}", timeout=10)

                if response.status_code != 200:
                    raise ValidationError({"places": "Place not found in Art Institute of Chicago API"})
                
                data = response.json()
                Place.objects.create(
                    travel=travel,
                    external_id=external_id,
                    title= data["data"]["title"]
                )

            travel.is_completed = not travel.places.filter(visited=False).exists()
            travel.save()


class TravelDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Travel.objects.all()
    serializer_class = TravelSerializer    


    def destroy(self, request, *args, **kwargs):
        travel = self.get_object()

        if travel.places.filter(visited=True).exists():
            return Response(
                {"error": "Can not delete travel with visited places"},
                status=400
            )

        return super().destroy(request, *args, **kwargs)


class PlaceListCreateAPIView(ListCreateAPIView):
    serializer_class = PlaceSerializer
    

    def get_queryset(self):
        travel = get_object_or_404(Travel, pk=self.kwargs['pk'])
        visited = self.request.GET.get("visited")

        if visited is not None:
            return travel.places.filter(visited=visited)
        return travel.places.all()


    def post(self, request, pk):
        travel = get_object_or_404(Travel, id=pk)

        external_id = request.data.get("external_id")
        if not external_id:
            return Response({'error': 'external_id is required'}, status=400)

        if travel.places.count() >=10:
            return Response({'error': 'Maximum 10 places per project.'}, status=400)
        

        if Place.objects.filter(travel=travel, external_id=external_id).exists():
            return Response({"error": "Place already exists in this project"}, status=400)
        

        response = requests.get(f"https://api.artic.edu/api/v1/artworks/{external_id}", timeout=10)

        if response.status_code != 200:
            return Response({'error': 'Place not found in Art Institute of Chicago API'}, status=404)
        
        data = response.json()

        
        place = Place.objects.create(
            travel = travel,
            external_id = external_id,
            title = data['data']['title'],
            notes = request.data.get('notes')
        )

        sr_data = PlaceSerializer(place).data

        return Response(sr_data, status=201)


class PlaceRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = PlaceSerializer
    http_method_names = ['get', 'patch']


    def get_object(self):
        place_id = self.kwargs['place_pk']
        travel_id = self.kwargs['travel_pk']

        place = get_object_or_404(Place, travel_id=travel_id, pk=place_id)

        return place
    
    
    def perform_update(self, serializer):
        place = serializer.save()

        travel = place.travel
        travel.is_completed = not travel.places.filter(visited=False).exists()
        travel.save()
