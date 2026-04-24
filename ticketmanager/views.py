from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from rest_framework import generics
from .models import Event, Ticket
from .serializers import EventSerializer, TicketSerializer
from .forms import EventForm, TicketForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status

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
# VUES API DE CONNEXION
# ==========================
class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'username': user.username
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


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
