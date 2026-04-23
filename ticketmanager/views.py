from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from rest_framework import generics, permissions
from .models import Event, Ticket
from .serializers import EventSerializer, TicketSerializer, UserSerializer, UserCreateSerializer, UserUpdateSerializer
from .forms import EventForm, TicketForm
from django.contrib.auth.models import User
from .forms import UserCreateForm, UserUpdateForm

# ==========================
# VUES API (DRF)
# ==========================
class EventListCreateAPIView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class TicketListCreateAPIView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class TicketRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


# ==========================
# API: GESTION DES UTILISATEURS
# ==========================

class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all().order_by('username')
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return UserUpdateSerializer
        return UserSerializer


# ==========================
# VUES TEMPLATES (FRONTEND)
# ==========================

def home(request):
    return render(request, 'home.html')

def event_list(request):
    events = Event.objects.filter(is_active=True).order_by('date')
    return render(request, 'event_list.html', {'events': events})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    tickets = event.tickets.filter(is_active=True)
    return render(request, 'event_detail.html', {'event': event, 'tickets': tickets})

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

def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, "L'événement a été supprimé.")
        return redirect('frontend-event-list')
    return render(request, 'event_confirm_delete.html', {'event': event})

def ticket_add(request, event_id):
    """Ajouter une catégorie de tickets à un événement spécifique"""
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.event = event # On lie le ticket à l'événement
            ticket.save()
            messages.success(request, f"La catégorie de tickets a été ajoutée à {event.name}")
            return redirect('frontend-event-detail', pk=event.pk)
    else:
        form = TicketForm()
    
    return render(request, 'ticket_add.html', {'form': form, 'event': event})


# ==========================
# GESTION DES UTILISATEURS
# ==========================

def user_list(request):
    users = User.objects.all().order_by('username')
    return render(request, 'user_list.html', {'users': users})


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


def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "Utilisateur supprimé.")
        return redirect('frontend-user-list')
    return render(request, 'user_confirm_delete.html', {'user': user})
