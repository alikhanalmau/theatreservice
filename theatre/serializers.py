from rest_framework import serializers
from .models import Event, ExcursionOrder, ExcursionSlot, Review, TicketOrder, User
from django.contrib.auth import get_user_model


class EventSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'image']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'event', 'rating', 'comment', 'created_at', 'user']

    def get_user(self, obj):
        return {"username": obj.user.username}

class ExcursionSlotSerializer(serializers.ModelSerializer):
    available_slots = serializers.IntegerField(read_only=True)

    class Meta:
        model = ExcursionSlot
        fields = ['id', 'date', 'time', 'capacity', 'available_slots']


class ExcursionOrderSerializer(serializers.ModelSerializer):
    slot = ExcursionSlotSerializer(read_only=True)  # ← заменили на вложенный сериализатор

    class Meta:
        model = ExcursionOrder
        fields = ['id', 'slot', 'comment', 'created_at']

    def validate(self, data):
        user = self.context['request'].user
        slot = data.get('slot')

        if ExcursionOrder.objects.filter(user=user, slot=slot).exists():
            raise serializers.ValidationError("Вы уже записались на эту экскурсию.")

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        return ExcursionOrder.objects.create(user=user, **validated_data)


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user



class TicketOrderSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)

    class Meta:
        model = TicketOrder
        fields = ['id', 'event', 'count', 'comment', 'status', 'created_at']


class TicketOrderCreateSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())

    class Meta:
        model = TicketOrder
        fields = ['id', 'event', 'count', 'comment']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['status'] = 'reserved'
        return TicketOrder.objects.create(**validated_data)

