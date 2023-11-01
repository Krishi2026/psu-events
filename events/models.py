from django.db import models
from django.contrib.auth.models import User


# Model for the Venue Table
class Venue(models.Model):
	name = models.CharField('Venue Name', max_length=120)
	address = models.CharField(max_length=300)
	zip_code = models.CharField('Zip Code', max_length=15)
	phone = models.CharField('Contact Number', max_length=15, blank=True)
	web = models.URLField('Website Address',blank=True)
	email_address = models.EmailField('Email Address',blank=True)

	def __str__(self):
		return self.name


# Model for the Users Table
class Members(models.Model):
	first_name = models.CharField(max_length=40)
	last_name = models.CharField(max_length=40)
	email = models.EmailField('User Email ID')

	def __str__(self):
		return self.first_name+' '+self.last_name




# Model for the Events Table  
class Event(models.Model):
	name = models.CharField('Event Name', max_length=120)
	event_date = models.DateTimeField('Event Date', )
	venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
	manager =  models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
	description = models.TextField(blank=True)
	attendees = models.ManyToManyField(Members, blank=True)


	def __str__(self):
		return self.name

