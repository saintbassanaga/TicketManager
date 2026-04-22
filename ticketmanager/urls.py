from django.urls import path
from .views import (
    EventListCreateAPIView, 
    EventRetrieveUpdateDestroyAPIView,
    TicketListCreateAPIView,
    TicketRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    # URLs pour les Événements
    path('events/', EventListCreateAPIView.as_view(), name='event-list'),
    path('events/<int:pk>/', EventRetrieveUpdateDestroyAPIView.as_view(), name='event-detail'),

    # URLs pour les Tickets
    path('tickets/', TicketListCreateAPIView.as_view(), name='ticket-list'),
    path('tickets/<int:pk>/', TicketRetrieveUpdateDestroyAPIView.as_view(), name='ticket-detail'),
]
