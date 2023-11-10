from django.test import TestCase
from .models import Venue, Members, Event
from django.contrib.auth.models import User
import datetime
import warnings
from .forms import VenueForm
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

class VenueFormTest(TestCase):
    def test_venue_form_valid_data(self):
        # Create a dictionary with valid form data
        form_data = {
            'name': 'Example Venue',
            'address': '123 Main St',
            'zip_code': '12345',
            'phone': '123-456-7890',
            'web': 'http://example.com',
            'email_address': 'example@example.com',
        }

        # Create a form instance with the valid data
        form = VenueForm(data=form_data)

        # Check if the form is valid
        self.assertTrue(form.is_valid())

    def test_venue_form_invalid_data(self):
        # Create a dictionary with invalid form data (missing required field 'name')
        form_data = {
            'address': '123 Main St',
            'zip_code': '12345',
            'phone': '123-456-7890',
            'web': 'http://example.com',
            'email_address': 'example@example.com',
        }

        # Create a form instance with the invalid data
        form = VenueForm(data=form_data)

        # Check if the form is not valid
        self.assertFalse(form.is_valid())

    def test_venue_form_blank_data(self):
        # Create a form instance with no data
        form = VenueForm(data={})

        # Check if the form is not valid (since some fields are required)
        self.assertFalse(form.is_valid())

    def test_venue_form_labels(self):
        # Check if the labels are as expected
        form = VenueForm()
        self.assertEqual(form.fields['name'].label, '')
        self.assertEqual(form.fields['address'].label, '')
        self.assertEqual(form.fields['zip_code'].label, '')
        self.assertEqual(form.fields['phone'].label, '')
        self.assertEqual(form.fields['web'].label, '')
        self.assertEqual(form.fields['email_address'].label, '')

    def test_venue_form_widgets(self):
        # Check if the widgets are as expected
        form = VenueForm()
        self.assertEqual(form.fields['name'].widget.attrs, {'class': 'form-control', 'placeholder': 'Venue Name'})
        self.assertEqual(form.fields['address'].widget.attrs, {'class': 'form-control', 'placeholder': 'Address'})
        self.assertEqual(form.fields['zip_code'].widget.attrs, {'class': 'form-control', 'placeholder': 'Zip Code'})
        self.assertEqual(form.fields['phone'].widget.attrs, {'class': 'form-control', 'placeholder': 'Phone'})
        self.assertEqual(form.fields['web'].widget.attrs, {'class': 'form-control', 'placeholder': 'Web Address'})
        self.assertEqual(form.fields['email_address'].widget.attrs, {'class': 'form-control', 'placeholder': 'Email'})


