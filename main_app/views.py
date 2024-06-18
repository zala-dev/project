from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import VolunteeringEvent, Like
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def home(request):
  return render(request, 'home.html')

class EventListView(LoginRequiredMixin, ListView):
    model = VolunteeringEvent
    template_name = 'event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        # Get the events created by the logged-in user and order them by date and time 
        return VolunteeringEvent.objects.filter(organizer=self.request.user).order_by('date', 'time')
    
class EventDetailView(LoginRequiredMixin, DetailView):
    model = VolunteeringEvent
    template_name = 'event_detail.html'
    context_object_name = 'event'

    #Raise a 403 no permission error if the event was not created by the logged-in user 
    def get_object(self, queryset=None):
        event = super().get_object(queryset)
        if self.request.user != event.organizer:
            return self.handle_no_permission()
        return event

class EventCreateView(LoginRequiredMixin, CreateView):
    model = VolunteeringEvent
    template_name = 'event_form.html'
    fields = ['title', 'description', 'date', 'time', 'location', 'volunteers_needed']
    success_url = reverse_lazy('event_list')

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        return super().form_valid(form)

class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = VolunteeringEvent
    template_name = 'event_form.html'
    fields = ['title', 'description', 'date', 'time', 'location', 'volunteers_needed']
    success_url = reverse_lazy('event_list')

    def dispatch(self, request, *args, **kwargs):
        event = self.get_object()
        if event.organizer != self.request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = VolunteeringEvent
    template_name = 'event_confirm_delete.html'
    success_url = reverse_lazy('event_list')

    def dispatch(self, request, *args, **kwargs):
        event = self.get_object()
        if event.organizer != self.request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class MyVolunteeringEventsListView(LoginRequiredMixin, ListView):
    model = VolunteeringEvent
    template_name = 'my_volunteering_events.html'
    context_object_name = 'my_events'
    ordering = ['date', 'time']

    def get_queryset(self):
        event = self.request.user.volunteering_events.all()
        event = event.order_by(*self.ordering)
        return event

class AllVolunteeringEventsListView(LoginRequiredMixin, ListView):
    model = VolunteeringEvent
    template_name = 'all_events.html'
    context_object_name = 'events'
    ordering = ['date', 'time']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['liked_events'] = set(user.like_set.values_list('event_id', flat=True)) if user.is_authenticated else set()
        return context

class VolunteeringEventDetailView(LoginRequiredMixin, DetailView):
    model = VolunteeringEvent
    template_name = 'volunteering_event_detail.html'
    context_object_name = 'event'
        
@login_required
def add_volunteer(request, event_id):
    event = get_object_or_404(VolunteeringEvent, id=event_id)
    if not request.user in event.volunteers.all():
        event.volunteers.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def withdraw_volunteer(request, event_id):
    event = get_object_or_404(VolunteeringEvent, id=event_id)
    if request.user in event.volunteers.all():
        event.volunteers.remove(request.user)
    return redirect(request.META.get('HTTP_REFERER', '/'))
      
@login_required
def like_event(request, event_id):
    event = get_object_or_404(VolunteeringEvent, pk=event_id)
    Like.objects.get_or_create(user=request.user, event=event)
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def unlike_event(request, event_id):
    event = get_object_or_404(VolunteeringEvent, pk=event_id)
    Like.objects.filter(user=request.user, event=event).delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('/all-events')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)