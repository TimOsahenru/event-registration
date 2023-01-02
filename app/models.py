from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True, blank=True)
    hackathon_participant = models.BooleanField(default=True, null=True)
    # avatar =

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Event(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(null=True, blank=True)
	participation = models.ManyToManyField(User, blank=True, related_name='events')
	start_date = models.DateTimeField(null=True)
	end_date = models.DateTimeField()
	registration_deadline = models.DateTimeField(null=True)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.name
		
		
class Submission(models.Model):
	participant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='submissions')
	event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
	details = models.TextField(null=True, blank=True)
	
	def __str__(self):
		return str(self.participant) + '---' + str(self.event)
		
