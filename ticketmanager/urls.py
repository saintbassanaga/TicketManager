from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    # API Views
    EventListCreateAPIView, 
    EventRetrieveUpdateDestroyAPIView,
    TicketListCreateAPIView,
    TicketRetrieveUpdateDestroyAPIView,
    # Frontend Views
    home,
    event_list,
    event_detail,
    event_add,
    event_edit,
    event_delete,
    ticket_add
)

urlpatterns = [
    # --- Vues Frontend (HTML) ---
    path('', home, name='frontend-home'),
    path('events/', event_list, name='frontend-event-list'),
    path('concert/<int:pk>/', event_detail, name='frontend-event-detail'),
    path('concert/add/', event_add, name='frontend-event-add'),
    path('concert/<int:pk>/edit/', event_edit, name='frontend-event-edit'),
    path('concert/<int:pk>/delete/', event_delete, name='frontend-event-delete'),
    
    # Tickets
    path('concert/<int:event_id>/tickets/add/', ticket_add, name='frontend-ticket-add'),

    # --- Vues API (JSON) ---
    path('api/events/', EventListCreateAPIView.as_view(), name='event-list'),
    path('api/events/<int:pk>/', EventRetrieveUpdateDestroyAPIView.as_view(), name='event-detail'),
    path('api/tickets/', TicketListCreateAPIView.as_view(), name='ticket-list'),
    path('api/tickets/<int:pk>/', TicketRetrieveUpdateDestroyAPIView.as_view(), name='ticket-detail'),
]
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
