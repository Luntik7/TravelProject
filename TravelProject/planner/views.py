from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
import requests
from .models import Travel, Place
from .serializers import TravelSerializer, PlaceSerializer
from rest_framework.exceptions import MethodNotAllowed, ValidationError
from django.core import exceptions
from .services import get_artworks_data


# Create your views here.
class ArtSearchAPIView(APIView):
    def get(self, request):
        page = request.GET.get("page", 1)

        data = get_artworks_data(page)

        return Response({
            "data": data.get("data"),
            "pagination": data.get("pagination")
        })
    

class TravelViewSet(ModelViewSet):
    queryset = Travel.objects.all()
    serializer_class = TravelSerializer

    
    def perform_destroy(self, instance):
        try:
            instance.delete()
        except exceptions.ValidationError as e:
            raise ValidationError(str(e))
        

class PlaceViewSet(ModelViewSet):
    serializer_class = PlaceSerializer


    def get_queryset(self):
        return Place.objects.filter(travel_id=self.kwargs.get('travel_pk')) #travel_pk from nested router


    def perform_create(self, serializer):
        travel_id = self.kwargs.get('travel_pk')
        serializer.save(travel_id=travel_id)
        

    def perform_update(self, serializer):
        instance = serializer.instance
        new_external_id = serializer.validated_data.get('external_id', None)
        if new_external_id and instance.external_id != new_external_id:
            raise ValidationError("external_id cannot be changed")
        serializer.save()


    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed("Delete")


