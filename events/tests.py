from django.test import TestCase, Client
from django.urls import reverse


from .models import Venue, Members, Event
from django.contrib.auth.models import User
import datetime
import warnings
warnings.simplefilter('ignore')

class VenueModelTestCase(TestCase):

    def setUp(self):
        self.venue = Venue.objects.create(
            name="SMSU HALL",
            address="1825 SW Broadway, Portland, OR",
            zip_code="97201",
            phone="5037252663",
            web="https://www.pdx.edu/student-union/",
            email_address="meetings@pdx.edu"
        )

    def test_string(self):
        self.assertEqual(str(self.venue), "SMSU HALL")

    def test_venue_creation(self):
        self.assertIsInstance(self.venue, Venue)
        self.assertEqual(self.venue.name, "SMSU HALL")

    def test_venue_fields(self):
        self.assertEqual(self.venue.address, "1825 SW Broadway, Portland, OR")
        self.assertEqual(self.venue.zip_code, "97201")
        self.assertEqual(self.venue.phone, "5037252663")
        self.assertEqual(self.venue.web, "https://www.pdx.edu/student-union/")
        self.assertEqual(self.venue.email_address, "meetings@pdx.edu")

class MembersModelTestCase(TestCase):

    def setUp(self):
        self.member = Members.objects.create(
            first_name="Hanesh",
            last_name="Koganti",
            email="hanesh.koganti@gmail.com"
        )

    def test_string(self):
        self.assertEqual(str(self.member), "Hanesh Koganti")

    def test_members_creation(self):
        self.assertIsInstance(self.member, Members)
        self.assertEqual(self.member.first_name, "Hanesh")
        self.assertEqual(self.member.last_name, "Koganti")

    def test_members_email(self):
        self.assertEqual(self.member.email, "hanesh.koganti@gmail.com")

class EventModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='admin')
        self.venue = Venue.objects.create(name="Event Venue")
        self.member = Members.objects.create(first_name="Hanesh", last_name="Koganti")
        self.event_date = datetime.datetime.now()
        self.event = Event.objects.create(
            name="Diwali",
            event_date=self.event_date,
            venue=self.venue,
            manager=self.user
        )

    def test_string(self):
        self.assertEqual(str(self.event), "Diwali")

    def test_event_creation(self):
        self.assertIsInstance(self.event, Event)
        self.assertEqual(self.event.name, "Diwali")
        self.assertEqual(self.event.event_date, self.event_date)
        self.assertEqual(self.event.venue, self.venue)

    def test_event_relation(self):
        self.event.attendees.add(self.member)
        self.assertIn(self.member, self.event.attendees.all())
        self.assertEqual(self.event.manager, self.user)


class URLTest(TestCase):
    def test_home_url(self):
        url = reverse('home')
        self.assertEqual(url, '/') 


    def test_events_url(self):
        url = reverse('list-events')
        self.assertEqual(url, '/events/')  

    def test_add_venue_url(self):
        url = reverse('add-venue')
        self.assertEqual(url, '/add_venue/')  

    def test_list_venues_url(self):
        url = reverse('list-venues')
        self.assertEqual(url, '/list_venues/') 

    def test_show_venue_url(self):
        venue_id = 1  
        url = reverse('show-venue', args=[venue_id])
        self.assertEqual(url, f'/show_venue/{venue_id}/') 

    def test_search_venues_url(self):
        url = reverse('search-venues')
        self.assertEqual(url, '/search_venues/')  

    def test_views(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)  
