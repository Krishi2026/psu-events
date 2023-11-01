from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from .models import Event, Venue
from .forms import VenueForm





def all_events(request):
	event_list = Event.objects.all()
	return render(request, 'events/event_list.html',
		{"event_list": event_list})







def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	#Converting month to uppercase
	month = month.capitalize()
	# Month Conversation
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	#Calender
	cal = HTMLCalendar().formatmonth(
		year,
		month_number)

	#Current Time and Year
	current_time = datetime.now()
	current_year = current_time.year
	return render(request,'events/home.html',{
	"year": year,
	"month": month,
	"month_number":month_number,
	"cal": cal,
	"current_year": current_year,
		})
