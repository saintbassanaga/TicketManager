from django.db import models
from django.contrib.auth.models import User

# Modèle pour les événements de concert
class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# Modèle pour les types de tickets disponibles pour un concert
class Ticket(models.Model):
    # Choix simples pour le type de ticket
    TICKET_TYPES = (
        ('STD', 'Standard'),
        ('VIP', 'VIP'),
        ('VVP', 'VVIP'),
    )

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    ticket_type = models.CharField(max_length=3, choices=TICKET_TYPES, default='STD')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.event.name} - {self.get_ticket_type_display()}"

# Modèle pour la commande globale d'un utilisateur
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Commande {self.id} par {self.user.username}"

# Modèle pour chaque article (ticket) dans une commande
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.ticket.ticket_type} pour {self.order.id}"
