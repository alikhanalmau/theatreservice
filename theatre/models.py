from django.db import models
from django.contrib.auth.models import AbstractUser

from abai_theatre import settings

class User(AbstractUser):
    role = models.CharField(max_length=50, default='user')  # или 'admin', 'manager'


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    image = models.ImageField(upload_to='events/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ExcursionSlot(models.Model):
    date = models.DateField()
    time = models.TimeField()
    capacity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} {self.time} (мест: {self.capacity})"

    @property
    def booked_count(self):
        return self.orders.count()

    @property
    def available_slots(self):
        return self.capacity - self.booked_count


class ExcursionOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slot = models.ForeignKey(ExcursionSlot, on_delete=models.CASCADE, related_name="orders", null=True)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.slot.date} {self.slot.time}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



class TicketOrder(models.Model):
    STATUS_CHOICES = [
        ('reserved', 'Забронировано'),
        ('paid', 'Оплачено'),
        ('cancelled', 'Отменено'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reserved')
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} → {self.event.title} ({self.count} шт.)'