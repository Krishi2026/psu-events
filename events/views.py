from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from .models import Event, Venue
from .forms import VenueForm, EventForm, EventFormAdmin
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User

def show_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	venue_owner = User.objects.get(pk=venue.owner)
	events = venue.event_set.all()
	return render(request, 'events/show_venue.html', 
		{'venue': venue,
		'venue_owner':venue_owner,
		'events':events})


def update_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	form = VenueForm(request.POST or None, instance=venue)
	if form.is_valid():
		form.save()
		return redirect('list-venues')
	return render(request, 'events/update_venue.html',
		{'venue':venue, 
   		'form':form})

def all_events(request):
	event_list = Event.objects.all().order_by('name')
	return render(request, 'events/event_list.html',
		{"event_list": event_list})

def add_event(request):
	submitted = False
	if request.method == "POST":
		if request.user.is_superuser:
			form = EventFormAdmin(request.POST)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/add_event?submitted=True')
		else:
			form = EventForm(request.POST)
			if form.is_valid():
				# form.save()
				event = form.save(commit=False)
				event.manager = request.user #logged in user
				event.save()
				return HttpResponseRedirect('/add_event?submitted=True')
	else:
		#Just going to the page, not submitting
		if request.user.is_superuser:
			form = EventFormAdmin
		else:
			form = EventForm
		if 'submitted' in request.GET:
			submitted = True
	return render(request, 'events/add_event.html',
		{'form':form,'submitted':submitted})


def my_events(request):
	if request.user.is_authenticated:
		me = request.user.id
		events = Event.objects.filter(attendees=me)
		return render(request, 
			'events/my_events.html', {
				"events":events
			})

	else:
		messages.success(request, ("You Aren't Authorized To View This Page"))
		return redirect('home')

def delete_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	venue.delete()
	return redirect('list-venues')		


def search_events(request):
	if request.method == "POST":
		searched = request.POST['searched']
		events = Event.objects.filter(description__contains=searched)
	
		return render(request, 
		'events/search_events.html', 
		{'searched':searched,
		'events':events})
	else:
		return render(request, 
		'events/search_events.html', 
		{})

def update_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	if request.user.is_superuser:
		form = EventFormAdmin(request.POST or None, instance=event)
	else:
		form = EventForm(request.POST or None, instance=event)
	if form.is_valid():
		form.save()
		return redirect('list-events')
	return render(request, 'events/update_event.html',
		{'event':event, 
   		'form':form})

def delete_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	event.delete()
	return redirect('list-events')


def delete_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	if request.user == event.manager:
		event.delete()
		messages.success(request, ("Event Deleted successfully"))
		return redirect('list-events')		
	else:
		messages.success(request, ("You Aren't Authorized To Delete This Event!"))
		return redirect('list-events')	


def list_venues(request):
	venue_list = Venue.objects.all()
	return render(request, 'events/venue.html',
		{'venue_list':venue_list})


def search_venues(request):
	if request.method == "POST":
		searched = request.POST['searched']
		venues = Venue.objects.filter(name__contains=searched)

		return render(request, 'events/search_venues.html',
		{'searched':searched,'venues':venues})
	else:
		return render(request, 'events/search_venues.html',
		{})

def add_venue(request):
	submitted = False
	if request.method == "POST":
		form = VenueForm(request.POST)
		if form.is_valid():
			venue = form.save(commit=False)
			venue.owner = request.user.id #logged in user
			venue.save()
			# form.save()
			return HttpResponseRedirect('/add_venue?submitted=True')

	else:
		form = VenueForm
		if 'submitted' in request.GET:
			submitted = True
	return render(request, 'events/add_venue.html',
		{'form':form,'submitted':submitted})


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	name = "Honey"
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)
	cal = HTMLCalendar().formatmonth(
		year, 
		month_number)
	now = datetime.now()
	current_year = now.year
	event_list = Event.objects.filter(
		event_date__year = year,
		event_date__month = month_number
		)
	time = now.strftime('%I:%M %p')
	return render(request, 
		'events/home.html', {
		"name": name,
		"year": year,
		"month": month,
		"month_number": month_number,
		"cal": cal,
		"current_year": current_year,
		"time":time,
		"event_list": event_list,
		})