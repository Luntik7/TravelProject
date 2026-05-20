from rest_framework import serializers

from planner.services import get_title_by_external_id
from .models import Travel, Place
from django.db import IntegrityError, transaction
from rest_framework.exceptions import ValidationError


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = [
            "id",
            "title",
            "notes",
            "external_id",
            "visited",
            "travel"
        ]

        read_only_fields = ["id", "title", "travel"]


    @classmethod
    def update_travel_complete(cls, travel):
        is_completed = travel.places.exists() and not travel.places.filter(visited=False).exists()
        if travel.is_completed != is_completed:
            travel.is_completed = is_completed
            travel.save()


    def create(self, validated_data):
        with transaction.atomic():
            travel = Travel.objects.select_for_update().get(pk=validated_data.get('travel_id'))
            if travel.places.count() >= 10:
                raise ValidationError("Travel can contain at max 10 places")
            
            title = get_title_by_external_id(validated_data['external_id'])
            validated_data['title']=title

            try:
                instance = super().create(validated_data)
            except IntegrityError:
                raise ValidationError("This place already exists in this travel")
            
            self.update_travel_complete(travel)
            
            return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        self.update_travel_complete(instance.travel)
        return instance


class PlaceInputSerializer(serializers.Serializer):
    notes = serializers.CharField(required=False)
    external_id = serializers.IntegerField()
    visited = serializers.BooleanField(default=False)


class TravelSerializer(serializers.ModelSerializer):
    places = PlaceInputSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Travel
        fields = [
            "id",
            "name",
            "description",
            "start_date",
            "is_completed",
            "places",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "is_completed"]

    
    def create(self, validated_data):
        places_data = validated_data.pop("places", [])

        if len(places_data) > 10:
            raise ValidationError("Travel can contain at max 10 places")

        with transaction.atomic():
            travel = Travel.objects.create(**validated_data)
            
            for place in places_data:
                title = get_title_by_external_id(place['external_id'])
                Place.objects.create(
                    title=title,
                    notes=place.get('notes', None),
                    external_id=place['external_id'],
                    visited=place.get('visited', False),
                    travel=travel,
                )

            PlaceSerializer.update_travel_complete(travel)

        return travel