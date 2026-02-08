# bookings/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Booking
from .serializers import BookingSerializer
from django.shortcuts import get_object_or_404

class BookingView(APIView):

    # 🔹 GET: সব booking + client name
    def get(self, request):
        bookings = Booking.objects.select_related("client_id").all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 🔹 POST: booking create
    def post(self, request):
        serializer = BookingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )



class BookingDetailView(APIView):

    def get(self, request, booking_id):
        booking = get_object_or_404(
            Booking.objects.select_related("client_id"),
            id=booking_id
        )
        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        booking.delete()
        return Response(
            {"message": "Booking deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )