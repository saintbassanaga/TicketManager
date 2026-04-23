from rest_framework import serializers
from .models import Event, Ticket, Order, OrderItem

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'event', 'ticket_type', 'price', 'quantity_available', 'is_active']

class EventSerializer(serializers.ModelSerializer):
    # Permet de voir les tickets associés lors de la consultation d'un événement
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'date', 'location', 'is_active', 'tickets']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'ticket', 'quantity', 'price_at_purchase']

class OrderSerializer(serializers.ModelSerializer):
    # Permet de voir les items associés lors de la consultation d'une commande
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'order_date', 'total_amount', 'is_paid', 'items']
