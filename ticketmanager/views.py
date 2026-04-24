from functools import wraps
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Event, Ticket, Order, OrderItem
from .serializers import (
    EventSerializer, TicketSerializer,
    UserSerializer, UserCreateSerializer, UserUpdateSerializer,
    OrderSerializer, OrderItemSerializer,
)
from .forms import EventForm, TicketForm, UserCreateForm, UserUpdateForm, RegisterForm


# ==========================
# PERMISSIONS & DECORATEURS
# ==========================

class IsAdminOrReadOnly(permissions.BasePermission):
    """Lecture pour tout utilisateur authentifié, écriture réservée aux admins."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.is_staff


def admin_required(view_func):
    """Redirige vers l'accueil avec un message d'erreur si l'utilisateur n'est pas admin."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/login/?next={request.path}')
        if not request.user.is_staff:
            messages.error(request, "Accès réservé aux administrateurs.")
            return redirect('frontend-home')
        return view_func(request, *args, **kwargs)
    return wrapper


# ==========================
# VUES API (DRF)
# ==========================

class EventListCreateAPIView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminOrReadOnly]


class EventRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminOrReadOnly]


class TicketListCreateAPIView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAdminOrReadOnly]


class TicketRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAdminOrReadOnly]


class OrderListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all().order_by('-order_date')
        return Order.objects.filter(user=self.request.user).order_by('-order_date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)


class OrderItemListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return OrderItem.objects.all()
        return OrderItem.objects.filter(order__user=self.request.user)


class OrderItemRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return OrderItem.objects.all()
        return OrderItem.objects.filter(order__user=self.request.user)


class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all().order_by('username')
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return UserUpdateSerializer
        return UserSerializer


# ==========================
# API LOGIN (publique)
# ==========================

class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'username': user.username,
                'is_staff': user.is_staff,
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# ==========================
# AUTHENTIFICATION (publique)
# ==========================

def login_view(request):
    if request.user.is_authenticated:
        return redirect('frontend-home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'frontend-home')
            return redirect(next_url)
        messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, 'login.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "Vous avez été déconnecté.")
    return redirect('frontend-login')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('frontend-home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Bienvenue {user.username} ! Votre compte a été créé.")
            return redirect('frontend-home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


# ==========================
# FRONTEND — utilisateur connecté
# ==========================

@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def event_list(request):
    events = Event.objects.filter(is_active=True).order_by('date')
    return render(request, 'event_list.html', {'events': events})


@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    tickets = event.tickets.filter(is_active=True)
    return render(request, 'event_detail.html', {'event': event, 'tickets': tickets})


# ==========================
# FRONTEND — admin uniquement
# ==========================

@admin_required
def event_add(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "L'événement a été créé avec succès !")
            return redirect('frontend-event-list')
    else:
        form = EventForm()
    return render(request, 'event_add.html', {'form': form})


@admin_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "L'événement a été mis à jour avec succès !")
            return redirect('frontend-event-detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'event_add.html', {'form': form, 'edit_mode': True})


@admin_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, "L'événement a été supprimé.")
        return redirect('frontend-event-list')
    return render(request, 'event_confirm_delete.html', {'event': event})


@admin_required
def ticket_add(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.event = event
            ticket.save()
            messages.success(request, f"La catégorie de tickets a été ajoutée à {event.name}")
            return redirect('frontend-event-detail', pk=event.pk)
    else:
        form = TicketForm()
    return render(request, 'ticket_add.html', {'form': form, 'event': event})


@admin_required
def user_list(request):
    users = User.objects.all().order_by('username')
    return render(request, 'user_list.html', {'users': users})


@admin_required
def user_add(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Utilisateur créé avec succès.")
            return redirect('frontend-user-list')
    else:
        form = UserCreateForm()
    return render(request, 'user_add.html', {'form': form})


@admin_required
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Utilisateur mis à jour avec succès.")
            return redirect('frontend-user-list')
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'user_add.html', {'form': form, 'edit_mode': True, 'user_obj': user})


@admin_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "Utilisateur supprimé.")
        return redirect('frontend-user-list')
    return render(request, 'user_confirm_delete.html', {'user': user})


# ==========================
# RÉSERVATION — utilisateur connecté
# ==========================

@login_required
def reserve_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id, is_active=True)

    if ticket.quantity_available == 0:
        messages.error(request, "Ce ticket est complet.")
        return redirect('frontend-event-detail', pk=ticket.event.pk)

    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
        except (ValueError, TypeError):
            quantity = 0

        if quantity < 1:
            messages.error(request, "La quantité doit être au moins 1.")
        elif quantity > ticket.quantity_available:
            messages.error(request, f"Seulement {ticket.quantity_available} place(s) disponible(s).")
        else:
            with transaction.atomic():
                t = Ticket.objects.select_for_update().get(pk=ticket_id)
                if quantity > t.quantity_available:
                    messages.error(request, "Plus assez de places disponibles, veuillez réessayer.")
                else:
                    order = Order.objects.create(
                        user=request.user,
                        total_amount=t.price * quantity,
                    )
                    OrderItem.objects.create(
                        order=order,
                        ticket=t,
                        quantity=quantity,
                        price_at_purchase=t.price,
                    )
                    t.quantity_available -= quantity
                    t.save()
                    messages.success(request, f"Réservation confirmée ! {quantity} ticket(s) pour {t.event.name}.")
                    return redirect('my-orders')

    return render(request, 'reserve_ticket.html', {'ticket': ticket})


@login_required
def my_orders(request):
    orders = (Order.objects
              .filter(user=request.user)
              .order_by('-order_date')
              .prefetch_related('items__ticket__event'))
    return render(request, 'my_orders.html', {'orders': orders})
