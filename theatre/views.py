from rest_framework import generics
from .models import Event, ExcursionSlot, Review, ExcursionOrder, TicketOrder
from .serializers import (
    EventSerializer, ExcursionSlotSerializer, ReviewSerializer,
    ExcursionOrderSerializer, TicketOrderSerializer, UserRegisterSerializer
)
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from theatre import serializers

class EventListAPIView(generics.ListAPIView):
    queryset = Event.objects.all().order_by('date')
    serializer_class = EventSerializer

class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ExcursionSlotListAPIView(generics.ListAPIView):
    queryset = ExcursionSlot.objects.all().order_by('date')
    serializer_class = ExcursionSlotSerializer


class ExcursionOrderAPIView(generics.CreateAPIView):
    queryset = ExcursionOrder.objects.all()
    serializer_class = ExcursionOrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        slot = serializer.validated_data['slot']
        if slot.orders.count() >= slot.capacity:
            raise serializers.ValidationError("На эту экскурсию больше нельзя записаться.")
        serializer.save(user=self.request.user)


class UserRegisterAPIView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserRegisterSerializer



class ExcursionOrderAPIView(generics.CreateAPIView):
    queryset = ExcursionOrder.objects.all()
    serializer_class = ExcursionOrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketOrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = TicketOrder.objects.all()
    serializer_class = TicketOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TicketOrder.objects.filter(user=self.request.user).select_related('event')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class MyExcursionOrdersAPIView(generics.ListAPIView):
    serializer_class = ExcursionOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ExcursionOrder.objects.select_related('slot').filter(user=self.request.user).order_by('-created_at')


class ReviewCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        event_id = self.request.query_params.get('event')
        if event_id:
            return Review.objects.filter(event_id=event_id).order_by('-created_at')
        return Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)