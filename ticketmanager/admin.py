from django.contrib import admin
from .models import Event, Ticket, Order, OrderItem

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location', 'is_active')
    list_filter = ('is_active', 'date')
    search_fields = ('name', 'location')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('event', 'ticket_type', 'price', 'quantity_available', 'is_active')
    list_filter = ('ticket_type', 'is_active')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_date', 'total_amount', 'is_paid')
    list_filter = ('is_paid', 'order_date')
    inlines = [OrderItemInline]
