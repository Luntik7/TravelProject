from rest_framework import serializers
from .models import Travel, Place


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

        read_only_fields = ["id", "title", "travel", "external_id"]


class PlaceInputSerializer(serializers.Serializer):
    external_id = serializers.IntegerField()


class TravelSerializer(serializers.ModelSerializer):
    places = PlaceInputSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Travel
        fields = [
            "id",
            "title",
            "notes",
            "start_date",
            "created_at",
            "updated_at",
            "is_completed",
            "places",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "is_completed"]