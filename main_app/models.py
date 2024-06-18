from django.db import models
from django.urls import reverse
from datetime import datetime, date
from django.contrib.auth.models import User

class VolunteeringEvent(models.Model):

    def default_time():
        return datetime.now().time()

    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(default=date.today)
    time = models.TimeField(default=default_time)
    location = models.CharField(max_length=255)
    volunteers_needed = models.PositiveIntegerField(default=1)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    volunteers = models.ManyToManyField(User, related_name='volunteering_events', blank=True)

    def __str__(self):
        return self.title

    def volunteer_count(self):
        return self.volunteers.count()
    
    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'pk': self.id})

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey('VolunteeringEvent', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} likes {self.event.title}"