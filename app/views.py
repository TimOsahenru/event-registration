from django.shortcuts import render, redirect
from .models import User, Event, Submission


def home_page(request):
	users = User.objects.filter(hackathon_participant=True)
	events = Event.objects.all()
	context = {'users':users, 'events':events}
	return render(request, 'home.html', context)
	
	
def event_page(request, pk):
	event = Event.objects.get(id=pk)
	context = {'event':event}
	return render(request, 'event.html', context)
	
	
def registration_confirmation(request, pk):
	event = Event.objects.get(id=pk)
	
	if request.method == 'POST':
		event.participation.add(request.user)
		return redirect('event', pk=event.id)
	context = {'event':event}
	return render(request, 'event_confirmation.html', context)
	
