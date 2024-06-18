from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('events/<int:event_id>/add_volunteer/', views.add_volunteer, name='add_volunteer'),
    path('events/<int:event_id>/withdraw_volunteer/', views.withdraw_volunteer, name='withdraw_volunteer'),
    path('events/create/', views.EventCreateView.as_view(), name='event_create'),
    path('events/<int:pk>/update/', views.EventUpdateView.as_view(), name='event_update'),
    path('events/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
    path('my-events/', views.MyVolunteeringEventsListView.as_view(), name='my_events'),
    path('all-events/', views.AllVolunteeringEventsListView.as_view(), name='all_events'),
    path('all-events/<int:pk>/', views.VolunteeringEventDetailView.as_view(), name='volunteering_event_detail'),
    path('like/<int:event_id>/', views.like_event, name='like_event'),
    path('unlike/<int:event_id>/', views.unlike_event, name='unlike_event'),
    path('accounts/signup/', views.signup, name='signup')
]

