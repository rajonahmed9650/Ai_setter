from rest_framework import serializers
from .models import Booking
from clients.models import Client
from clients.serializers import ClientSerializers


class BookingSerializer(serializers.ModelSerializer):

    # 🔹 GET response → client full data
    client = ClientSerializers(source="client_id", read_only=True)
    class Meta:
        model = Booking
        fields = (
            "id",
            "lead_id",
            "client_id",   # POST
            "client",      # GET
            "meeting_date",
            "meeting_time",
            "meeting_link",
            "note",
            "status",
        )

    def create(self, validated_data):
        """
        validated_data example:
        {
            'client_id': <Client object>,
            'meeting_date': ...,
            ...
        }
        """

        client = validated_data.pop("client_id")

        booking = Booking.objects.create(
            client_id=client,   # 👈 model field name
            **validated_data
        )
        return booking
