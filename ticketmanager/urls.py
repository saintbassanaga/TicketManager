from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    # API Views
    EventListCreateAPIView,
    EventRetrieveUpdateDestroyAPIView,
    TicketListCreateAPIView,
    TicketRetrieveUpdateDestroyAPIView,
    OrderListCreateAPIView,
    OrderRetrieveUpdateDestroyAPIView,
    OrderItemListCreateAPIView,
    OrderItemRetrieveUpdateDestroyAPIView,
    UserListCreateAPIView,
    UserRetrieveUpdateDestroyAPIView,
    LoginAPIView,
    # Frontend Views
    home,
    event_list,
    event_detail,
    event_add,
    event_edit,
    event_delete,
    ticket_add,
    user_list,
    user_add,
    user_edit,
    user_delete,
    login_view,
    logout_view,
)

urlpatterns = [
    # --- Authentification ---
    path('login/', login_view, name='frontend-login'),
    path('logout/', logout_view, name='frontend-logout'),

    # --- Vues Frontend (HTML) ---
    path('', home, name='frontend-home'),
    path('events/', event_list, name='frontend-event-list'),
    path('concert/<int:pk>/', event_detail, name='frontend-event-detail'),
    path('concert/add/', event_add, name='frontend-event-add'),
    path('concert/<int:pk>/edit/', event_edit, name='frontend-event-edit'),
    path('concert/<int:pk>/delete/', event_delete, name='frontend-event-delete'),
    
    # Tickets
    path('concert/<int:event_id>/tickets/add/', ticket_add, name='frontend-ticket-add'),

    # Users Frontend
    path('users/', user_list, name='frontend-user-list'),
    path('users/add/', user_add, name='frontend-user-add'),
    path('users/<int:pk>/edit/', user_edit, name='frontend-user-edit'),
    path('users/<int:pk>/delete/', user_delete, name='frontend-user-delete'),

    # Users API
    path('api/users/', UserListCreateAPIView.as_view(), name='user-list'),
    path('api/users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-detail'),

    # --- Vues API (JSON) ---
    path('api/events/', EventListCreateAPIView.as_view(), name='event-list'),
    path('api/events/<int:pk>/', EventRetrieveUpdateDestroyAPIView.as_view(), name='event-detail'),
    path('api/tickets/', TicketListCreateAPIView.as_view(), name='ticket-list'),
    path('api/tickets/<int:pk>/', TicketRetrieveUpdateDestroyAPIView.as_view(), name='ticket-detail'),
    path('api/orders/', OrderListCreateAPIView.as_view(), name='order-list'),
    path('api/orders/<int:pk>/', OrderRetrieveUpdateDestroyAPIView.as_view(), name='order-detail'),
    path('api/order-items/', OrderItemListCreateAPIView.as_view(), name='orderitem-list'),
    path('api/order-items/<int:pk>/', OrderItemRetrieveUpdateDestroyAPIView.as_view(), name='orderitem-detail'),
    path('api/login/', LoginAPIView.as_view(), name='api_login'),
]
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
