# tests.py
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from django.test import TestCase, Client
from django.urls import reverse
from bella_italia.models import Reservation
from bella_italia.forms import ReservationForm
from bella_italia.views import make_reservation, cancel_reservation
from bella_italia.utils import fetch_available_times, send_sms, generate_time_slots
from django.utils import timezone


class ReservationFormTests(TestCase):

    def test_form_initialization_with_available_times(self):
        # Mock a function that fetches available times
        def mock_fetch_available_times(date):
            if date == datetime.today().date():
                return ['12:00 PM', '1:00 PM', '2:00 PM']  # Sample available times
            else:
                return []  # Return empty list for other dates

        # Create a form instance with mock data
        form_data = {
            'name': 'John Doe',
            'phone_number': '1234567890',
            'guests': 4,
            'date': datetime.today().date(),
        }
        form = ReservationForm(fetch_available_times=mock_fetch_available_times, data=form_data)

        # Assert that the form is valid
        self.assertTrue(form.is_valid())

        # Assert that the choices for 'time' field are correctly populated
        self.assertEqual(form.fields['time'].choices, [('12:00 PM', '12:00 PM'), ('1:00 PM', '1:00 PM'), ('2:00 PM', '2:00 PM')])

    def test_form_validation_invalid_guests(self):
        # Create a form instance with invalid number of guests (less than minimum)
        form_data = {
            'name': 'John Doe',
            'phone_number': '1234567890',
            'guests': 0,  # Invalid guests number
            'date': datetime.today().date(),
        }
        form = ReservationForm(data=form_data)

        # Assert that the form is not valid
        self.assertFalse(form.is_valid())
        # Assert that the 'guests' field has a specific error
        self.assertIn('guests', form.errors.keys())
        self.assertIn('Ensure this value is greater than or equal to 1.', form.errors['guests'])

class ReservationViewTests(TestCase):

    def test_make_reservation_view(self):
        url = reverse('make_reservation')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/make_reservation.html')

    def test_cancel_reservation_view(self):
        reservation = Reservation.objects.create(name='Jane Doe', phone_number='9876543210', guests=2, date=datetime.today().date(), time='12:00 PM')
        url = reverse('cancel_reservation', args=[reservation.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/cancel_reservation.html')

    # Add more view tests as needed for different scenarios

class TestUtilsFunctions(TestCase):

    def test_generate_time_slots(self):
        # Test case for generating time slots
        start_time = datetime.strptime('10:00', '%H:%M')
        end_time = datetime.strptime('12:00', '%H:%M')
        expected_time_slots = ['10:00-11:00', '11:00-12:00']
        self.assertEqual(generate_time_slots(start_time, end_time), expected_time_slots)

    def test_fetch_available_times(self):
        # Test case for fetching available times based on the selected date
        selected_date_monday = datetime(2024, 7, 1)  # A Monday
        selected_date_sunday = datetime(2024, 7, 7)  # A Sunday

        # Mocking datetime to control the current date for testing
        with patch('bookings.utils.datetime') as mock_datetime:
            # Mock Monday
            mock_datetime.today.return_value.date.return_value = selected_date_monday.date()
            self.assertEqual(fetch_available_times(selected_date_monday), generate_time_slots(datetime.combine(selected_date_monday, datetime.strptime("10:00", '%H:%M').time()), datetime.combine(selected_date_monday, datetime.strptime("22:00", '%H:%M').time())))

            # Mock Sunday
            mock_datetime.today.return_value.date.return_value = selected_date_sunday.date()
            self.assertEqual(fetch_available_times(selected_date_sunday), [])

    @patch('bookings.utils.Client')
    def test_send_sms_success(self, MockClient):
        # Mocking Twilio client
        mock_twilio_client = MockClient()
        mock_message_instance = MagicMock()
        mock_twilio_client.messages.create.return_value = mock_message_instance
        mock_message_instance.sid = 'MOCK_SID'

        # Test case for successful SMS sending
        reservation = MagicMock()
        reservation.date = '2024-07-01'
        reservation.time = '12:00 PM'
        result = send_sms('+1234567890', reservation)

        self.assertTrue(result)
        mock_twilio_client.messages.create.assert_called_once()

    @patch('bookings.utils.Client')
    def test_send_sms_failure(self, MockClient):
        # Mocking Twilio client to simulate failure
        mock_twilio_client = MockClient()
        mock_twilio_client.messages.create.side_effect = Exception('Test failure')

        # Test case for failed SMS sending
        reservation = MagicMock()
        reservation.date = '2024-07-01'
        reservation.time = '12:00 PM'
        result = send_sms('+1234567890', reservation)

        self.assertFalse(result)
        mock_twilio_client.messages.create.assert_called_once()

class ViewsTestCase(TestCase):

    def setUp(self):
        # Create a sample reservation object for testing
        self.reservation = Reservation.objects.create(
            name='Test User',
            phone_number='1234567890',
            guests=4,
            date=datetime.today().date(),
            time='12:00 PM'
        )

    def test_index_view(self):
        # Test index view
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_make_reservation_view_get(self):
        # Test make_reservation view with GET request
        response = self.client.get(reverse('make_reservation'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations/make_reservation.html')
        self.assertIsInstance(response.context['form'], ReservationForm)

    @patch('bookings.views.send_sms')
    def test_make_reservation_view_post_valid_form(self, mock_send_sms):
        # Test make_reservation view with POST request and valid form data
        form_data = {
            'name': 'Test User',
            'phone_number': '1234567890',
            'guests': 4,
            'date': datetime.today().date(),
            'time': '12:00 PM'
        }
        response = self.client.post(reverse('make_reservation'), form_data)
        self.assertEqual(response.status_code, 302)  # Check if redirected
        self.assertEqual(response.url, reverse('reservation_confirmation', args=[1]))  # Assuming reservation_id is 1
        mock_send_sms.assert_called_once_with('1234567890', self.reservation)

    def test_make_reservation_view_post_invalid_form(self):
        # Test make_reservation view with POST request and invalid form data
        form_data = {
            'name': '',  # Invalid form data
            'phone_number': '123',  # Invalid form data
            'guests': 0,  # Invalid form data
            'date': datetime.today().date(),
            'time': '12:00 PM'
        }
        response = self.client.post(reverse('make_reservation'), form_data)
        self.assertEqual(response.status_code, 200)  # Form errors, should return to the form page
        self.assertFormError(response, 'form', 'name', 'This field is required.')  # Check specific form errors

    def test_reservation_confirmation_view(self):
        # Test reservation_confirmation view
        response = self.client.get(reverse('reservation_confirmation', args=[self.reservation.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations/reservation_confirmation.html')
        self.assertEqual(response.context['reservation'], self.reservation)

    def test_get_available_times_view(self):
        # Test get_available_times view
        date_str = datetime.today().strftime('%Y-%m-%d')
        response = self.client.get(reverse('get_available_times') + f'?date={date_str}')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {'times': fetch_available_times(datetime.today().date())})

    def test_cancellation_view(self):
        # Test cancellation view
        response = self.client.get(reverse('cancellation', args=[self.reservation.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations/cancellation.html')
        self.assertEqual(response.context['reservation'], self.reservation)

    def test_cancel_reservation_view(self):
        # Test cancel_reservation view
        response = self.client.post(reverse('cancel_reservation', args=[self.reservation.id]))
        self.assertEqual(response.status_code, 302)  # Check if redirected
        self.assertRedirects(response, reverse('cancellation_confirmation'))
        self.assertFalse(Reservation.objects.filter(id=self.reservation.id).exists())  # Check if reservation is deleted

    def test_cancellation_confirmation_view(self):
        # Test cancellation_confirmation view
        response = self.client.get(reverse('cancellation_confirmation'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations/cancellation_confirmation.html')


