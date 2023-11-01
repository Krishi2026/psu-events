from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
from datetime import datetime
def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	name = "Hanesh"
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
	"name": name,
	"year": year,
	"month": month,
	"month_number":month_number,
	"cal": cal,
	"current_year": current_year,
		})
