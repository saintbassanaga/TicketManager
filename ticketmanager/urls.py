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
    register_view,
    reserve_ticket,
    my_orders,
)

# Frontend HTML routes — no format suffixes
frontend_urlpatterns = [
    path('login/', login_view, name='frontend-login'),
    path('logout/', logout_view, name='frontend-logout'),
    path('register/', register_view, name='frontend-register'),
    path('', home, name='frontend-home'),
    path('events/', event_list, name='frontend-event-list'),
    path('concert/<int:pk>/', event_detail, name='frontend-event-detail'),
    path('concert/add/', event_add, name='frontend-event-add'),
    path('concert/<int:pk>/edit/', event_edit, name='frontend-event-edit'),
    path('concert/<int:pk>/delete/', event_delete, name='frontend-event-delete'),
    path('concert/<int:event_id>/tickets/add/', ticket_add, name='frontend-ticket-add'),
    path('tickets/<int:ticket_id>/reserve/', reserve_ticket, name='reserve-ticket'),
    path('my-orders/', my_orders, name='my-orders'),
    path('users/', user_list, name='frontend-user-list'),
    path('users/add/', user_add, name='frontend-user-add'),
    path('users/<int:pk>/edit/', user_edit, name='frontend-user-edit'),
    path('users/<int:pk>/delete/', user_delete, name='frontend-user-delete'),
]

# API routes — format suffixes apply (?format=json or .json)
api_urlpatterns = format_suffix_patterns([
    path('api/login/', LoginAPIView.as_view(), name='api_login'),
    path('api/events/', EventListCreateAPIView.as_view(), name='event-list'),
    path('api/events/<int:pk>/', EventRetrieveUpdateDestroyAPIView.as_view(), name='event-detail'),
    path('api/tickets/', TicketListCreateAPIView.as_view(), name='ticket-list'),
    path('api/tickets/<int:pk>/', TicketRetrieveUpdateDestroyAPIView.as_view(), name='ticket-detail'),
    path('api/orders/', OrderListCreateAPIView.as_view(), name='order-list'),
    path('api/orders/<int:pk>/', OrderRetrieveUpdateDestroyAPIView.as_view(), name='order-detail'),
    path('api/order-items/', OrderItemListCreateAPIView.as_view(), name='orderitem-list'),
    path('api/order-items/<int:pk>/', OrderItemRetrieveUpdateDestroyAPIView.as_view(), name='orderitem-detail'),
    path('api/users/', UserListCreateAPIView.as_view(), name='user-list'),
    path('api/users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-detail'),
], allowed=['json', 'html'])

urlpatterns = frontend_urlpatterns + api_urlpatterns
