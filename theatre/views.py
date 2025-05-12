from rest_framework import generics
from .models import Event, ExcursionSlot, Review, ExcursionOrder, TicketOrder
from .serializers import (
    EventSerializer, ExcursionOrderCreateSerializer, ExcursionSlotSerializer, ReviewSerializer,
    ExcursionOrderSerializer, TicketOrderSerializer, UserRegisterSerializer
)
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
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
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return ExcursionOrderCreateSerializer

class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
from .serializers import TicketOrderSerializer, TicketOrderCreateSerializer

class TicketOrderListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TicketOrder.objects.filter(user=self.request.user).select_related('event')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TicketOrderCreateSerializer
        return TicketOrderSerializer


class MyExcursionOrdersAPIView(generics.ListAPIView):
    serializer_class = ExcursionOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ExcursionOrder.objects.select_related('slot').filter(user=self.request.user).order_by('-created_at')


class MyExcursionCancelAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        try:
            excursion = ExcursionOrder.objects.get(pk=pk, user=request.user)
            excursion.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ExcursionOrder.DoesNotExist:
            return Response({'detail': 'Не найдено или нет доступа'}, status=status.HTTP_404_NOT_FOUND)

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



