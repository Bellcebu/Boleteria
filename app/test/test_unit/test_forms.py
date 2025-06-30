from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django import forms

from app.forms import (
    CategoryModelForm,
    VenueModelForm,
    EventModelForm,
    TicketPurchaseForm,
    TicketModelForm,
    PromotionForm,
    RatingModelForm,
    CommentForm,
    NotificationModelForm,
    RefundRequestForm,
    SignUpForm,
)


class CategoryModelFormTest(TestCase):
    
    def test_clean_name_valid(self):
        form = CategoryModelForm()
        form.cleaned_data = {'name': 'Valid Category'}
        self.assertEqual(form.clean_name(), 'Valid Category')
    
    def test_clean_name_with_whitespace(self):
        form = CategoryModelForm()
        form.cleaned_data = {'name': '  Valid Category  '}
        self.assertEqual(form.clean_name(), 'Valid Category')
    
    def test_clean_name_empty(self):
        form = CategoryModelForm()
        form.cleaned_data = {'name': ''}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_name()
        self.assertIn("El nombre no puede estar vacío", str(cm.exception))
    
    def test_clean_name_whitespace_only(self):
        form = CategoryModelForm()
        form.cleaned_data = {'name': '   '}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_name()
        self.assertIn("El nombre no puede estar vacío", str(cm.exception))
    
    def test_clean_name_too_short(self):
        form = CategoryModelForm()
        form.cleaned_data = {'name': 'ab'}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_name()
        self.assertIn("El nombre debe tener al menos 3 caracteres", str(cm.exception))
    
    def test_clean_name_none(self):
        form = CategoryModelForm()
        form.cleaned_data = {'name': None}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_name()
        self.assertIn("El nombre no puede estar vacío", str(cm.exception))
    
    def test_clean_description_valid(self):
        form = CategoryModelForm()
        form.cleaned_data = {'description': 'This is a valid description'}
        self.assertEqual(form.clean_description(), 'This is a valid description')
    
    def test_clean_description_with_whitespace(self):
        form = CategoryModelForm()
        form.cleaned_data = {'description': '  Valid description  '}
        self.assertEqual(form.clean_description(), 'Valid description')
    
    def test_clean_description_too_short(self):
        form = CategoryModelForm()
        form.cleaned_data = {'description': 'short'}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_description()
        self.assertIn("La descripción debe tener al menos 10 caracteres", str(cm.exception))
    
    def test_clean_description_empty(self):
        form = CategoryModelForm()
        form.cleaned_data = {'description': ''}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_description()
        self.assertIn("La descripción debe tener al menos 10 caracteres", str(cm.exception))
    
    def test_clean_is_active_true(self):
        form = CategoryModelForm()
        form.cleaned_data = {'is_active': True}
        self.assertTrue(form.clean_is_active())
    
    def test_clean_is_active_false(self):
        form = CategoryModelForm()
        form.cleaned_data = {'is_active': False}
        self.assertFalse(form.clean_is_active())
    

class VenueModelFormTest(TestCase):
    
    def test_clean_name_valid(self):
        form = VenueModelForm()
        form.cleaned_data = {'name': 'Valid Venue'}
        self.assertEqual(form.clean_name(), 'Valid Venue')
    
    def test_clean_name_with_whitespace(self):
        form = VenueModelForm()
        form.cleaned_data = {'name': '  Valid Venue  '}
        self.assertEqual(form.clean_name(), 'Valid Venue')
    
    def test_clean_name_too_short(self):
        form = VenueModelForm()
        form.cleaned_data = {'name': 'ab'}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_name()
        self.assertIn("El nombre debe tener al menos 3 caracteres", str(cm.exception))
    
    def test_clean_city_valid(self):
        form = VenueModelForm()
        form.cleaned_data = {'city': 'Buenos Aires'}
        self.assertEqual(form.clean_city(), 'Buenos Aires')
    
    def test_clean_city_empty(self):
        form = VenueModelForm()
        form.cleaned_data = {'city': ''}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_city()
        self.assertIn("La ciudad es obligatoria", str(cm.exception))
    
    def test_clean_city_numeric(self):
        form = VenueModelForm()
        form.cleaned_data = {'city': '12345'}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_city()
        self.assertIn("La ciudad no puede ser un número", str(cm.exception))
    
    def test_clean_address_valid(self):
        form = VenueModelForm()
        form.cleaned_data = {'address': 'Av. Corrientes 1234'}
        self.assertEqual(form.clean_address(), 'Av. Corrientes 1234')
    
    def test_clean_address_too_short(self):
        form = VenueModelForm()
        form.cleaned_data = {'address': 'Av'}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_address()
        self.assertIn("La dirección debe tener al menos 5 caracteres", str(cm.exception))
    
    def test_clean_contact_valid(self):
        form = VenueModelForm()
        form.cleaned_data = {'contact': '123-456-7890'}
        self.assertEqual(form.clean_contact(), '123-456-7890')
    
    def test_clean_contact_too_short(self):
        form = VenueModelForm()
        form.cleaned_data = {'contact': '123'}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_contact()
        self.assertIn("El contacto debe tener al menos 5 caracteres", str(cm.exception))
    
    def test_clean_capacity_valid(self):
        form = VenueModelForm()
        form.cleaned_data = {'capacity': 100}
        self.assertEqual(form.clean_capacity(), 100)
    
    def test_clean_capacity_zero(self):
        form = VenueModelForm()
        form.cleaned_data = {'capacity': 0}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_capacity()
        self.assertIn("La capacidad debe ser un número positivo", str(cm.exception))
    
    def test_clean_capacity_negative(self):
        form = VenueModelForm()
        form.cleaned_data = {'capacity': -5}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_capacity()
        self.assertIn("La capacidad debe ser un número positivo", str(cm.exception))
    
    def test_clean_capacity_none(self):
        form = VenueModelForm()
        form.cleaned_data = {'capacity': None}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_capacity()
        self.assertIn("La capacidad debe ser un número positivo", str(cm.exception))


class EventModelFormTest(TestCase):
    
    def test_clean_title_valid(self):
        form = EventModelForm()
        form.cleaned_data = {'title': 'Valid Event Title'}
        self.assertEqual(form.clean_title(), 'Valid Event Title')
    
    def test_clean_title_empty(self):
        form = EventModelForm()
        form.cleaned_data = {'title': ''}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_title()
        self.assertIn("El título es obligatorio", str(cm.exception))
    
    def test_clean_title_too_short(self):
        form = EventModelForm()
        form.cleaned_data = {'title': 'Hi'}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_title()
        self.assertIn("El título debe tener al menos 5 caracteres", str(cm.exception))
    
    def test_clean_description_valid(self):
        form = EventModelForm()
        form.cleaned_data = {'description': 'This is a valid event description'}
        self.assertEqual(form.clean_description(), 'This is a valid event description')
    
    def test_clean_description_empty(self):
        form = EventModelForm()
        form.cleaned_data = {'description': ''}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_description()
        self.assertIn("La descripción es obligatoria", str(cm.exception))
    
    def test_clean_description_too_short(self):
        form = EventModelForm()
        form.cleaned_data = {'description': 'Short desc'}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_description()
        self.assertIn("La descripción debe tener al menos 20 caracteres", str(cm.exception))
    
    def test_clean_date_valid(self):
        form = EventModelForm()
        test_date = datetime.now() + timedelta(days=1)
        form.cleaned_data = {'date': test_date}
        self.assertEqual(form.clean_date(), test_date)
    
    def test_clean_date_none(self):
        form = EventModelForm()
        form.cleaned_data = {'date': None}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_date()
        self.assertIn("La fecha es obligatoria", str(cm.exception))


class TicketPurchaseFormTest(TestCase):
    
    def test_clean_quantity_valid_without_ticket_tier(self):
        form = TicketPurchaseForm()
        form.cleaned_data = {'quantity': 5}
        self.assertEqual(form.clean_quantity(), 5)


class TicketModelFormTest(TestCase):
    
    def test_clean_name_valid(self):
        form = TicketModelForm()
        form.cleaned_data = {'name': 'VIP Ticket'}
        self.assertEqual(form.clean_name(), 'VIP Ticket')
    
    def test_clean_name_empty(self):
        form = TicketModelForm()
        form.cleaned_data = {'name': ''}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_name()
        self.assertIn("El nombre es obligatorio", str(cm.exception))
    
    def test_clean_price_valid(self):
        form = TicketModelForm()
        form.cleaned_data = {'price': 50.00}
        self.assertEqual(form.clean_price(), 50.00)
    
    def test_clean_price_zero(self):
        form = TicketModelForm()
        form.cleaned_data = {'price': 0}
        self.assertEqual(form.clean_price(), 0)
    
    def test_clean_price_negative(self):
        form = TicketModelForm()
        form.cleaned_data = {'price': -10}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_price()
        self.assertIn("El precio debe ser mayor o igual a 0", str(cm.exception))
    
    def test_clean_price_none(self):
        form = TicketModelForm()
        form.cleaned_data = {'price': None}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_price()
        self.assertIn("El precio debe ser mayor o igual a 0", str(cm.exception))
    
    def test_clean_max_quantity_valid(self):
        form = TicketModelForm()
        form.cleaned_data = {'max_quantity': 100}
        self.assertEqual(form.clean_max_quantity(), 100)
    
    def test_clean_max_quantity_zero(self):
        form = TicketModelForm()
        form.cleaned_data = {'max_quantity': 0}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_max_quantity()
        self.assertIn("La cantidad máxima debe ser mayor que 0", str(cm.exception))
    
    def test_clean_max_quantity_negative(self):
        form = TicketModelForm()
        form.cleaned_data = {'max_quantity': -5}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_max_quantity()
        self.assertIn("La cantidad máxima debe ser mayor que 0", str(cm.exception))


class PromotionFormTest(TestCase):
    
    def test_clean_code_valid(self):
        form = PromotionForm()
        form.cleaned_data = {'code': 'DISCOUNT20'}
        self.assertEqual(form.clean_code(), 'DISCOUNT20')
    
    def test_clean_code_lowercase_converted(self):
        form = PromotionForm()
        form.cleaned_data = {'code': 'discount20'}
        self.assertEqual(form.clean_code(), 'DISCOUNT20')
    
    def test_clean_code_empty(self):
        form = PromotionForm()
        form.cleaned_data = {'code': ''}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_code()
        self.assertIn("El código es obligatorio", str(cm.exception))
    
    def test_clean_code_too_short(self):
        form = PromotionForm()
        form.cleaned_data = {'code': 'AB'}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_code()
        self.assertIn("El código debe tener al menos 3 caracteres", str(cm.exception))
    
    def test_clean_discount_percentage_valid(self):
        form = PromotionForm()
        form.cleaned_data = {'discount_percentage': 25.5}
        self.assertEqual(form.clean_discount_percentage(), 25.5)
    
    def test_clean_discount_percentage_zero(self):
        form = PromotionForm()
        form.cleaned_data = {'discount_percentage': 0}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_discount_percentage()
        self.assertIn("El descuento debe estar entre 0.01 y 100", str(cm.exception))
    
    def test_clean_discount_percentage_over_100(self):
        form = PromotionForm()
        form.cleaned_data = {'discount_percentage': 150}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_discount_percentage()
        self.assertIn("El descuento debe estar entre 0.01 y 100", str(cm.exception))
    
    def test_clean_valid_dates(self):
        form = PromotionForm()
        start_date = datetime.now()
        end_date = datetime.now() + timedelta(days=7)
        form.cleaned_data = {
            'start_date': start_date,
            'end_date': end_date
        }
        self.assertEqual(form.clean(), form.cleaned_data)
    
    def test_clean_invalid_dates(self):
        form = PromotionForm()
        start_date = datetime.now() + timedelta(days=7)
        end_date = datetime.now()
        form.cleaned_data = {
            'start_date': start_date,
            'end_date': end_date
        }
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean()
        self.assertIn("La fecha de inicio debe ser anterior a la fecha de fin", str(cm.exception))


class RatingModelFormTest(TestCase):
    
    def test_clean_title_valid(self):
        form = RatingModelForm()
        form.cleaned_data = {'title': 'Great Event'}
        self.assertEqual(form.clean_title(), 'Great Event')
    
    def test_clean_title_empty(self):
        form = RatingModelForm()
        form.cleaned_data = {'title': ''}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_title()
        self.assertIn("El título es obligatorio", str(cm.exception))
    
    def test_clean_text_valid(self):
        form = RatingModelForm()
        form.cleaned_data = {'text': 'This was an amazing experience!'}
        self.assertEqual(form.clean_text(), 'This was an amazing experience!')
    
    def test_clean_text_empty(self):
        form = RatingModelForm()
        form.cleaned_data = {'text': ''}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_text()
        self.assertIn("El comentario es obligatorio", str(cm.exception))
    
    def test_clean_rating_valid(self):
        form = RatingModelForm()
        form.cleaned_data = {'rating': 4}
        self.assertEqual(form.clean_rating(), 4)
    
    def test_clean_rating_too_low(self):
        form = RatingModelForm()
        form.cleaned_data = {'rating': 0}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_rating()
        self.assertIn("La calificación debe estar entre 1 y 5", str(cm.exception))
    
    def test_clean_rating_too_high(self):
        form = RatingModelForm()
        form.cleaned_data = {'rating': 6}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_rating()
        self.assertIn("La calificación debe estar entre 1 y 5", str(cm.exception))


class CommentFormTest(TestCase):
    
    def test_clean_title_valid(self):
        form = CommentForm()
        form.cleaned_data = {'title': 'Comment Title'}
        self.assertEqual(form.clean_title(), 'Comment Title')
    
    def test_clean_title_empty(self):
        form = CommentForm()
        form.cleaned_data = {'title': ''}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_title()
        self.assertIn("El título es obligatorio", str(cm.exception))
    
    def test_clean_text_valid(self):
        form = CommentForm()
        form.cleaned_data = {'text': 'This is my comment'}
        self.assertEqual(form.clean_text(), 'This is my comment')
    
    def test_clean_text_empty(self):
        form = CommentForm()
        form.cleaned_data = {'text': ''}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_text()
        self.assertIn("El comentario es obligatorio", str(cm.exception))


class NotificationModelFormTest(TestCase):
    
    def test_clean_title_valid(self):
        form = NotificationModelForm()
        form.cleaned_data = {'title': 'Valid Title'}
        self.assertEqual(form.clean_title(), 'Valid Title')
    
    def test_clean_title_empty(self):
        form = NotificationModelForm()
        form.cleaned_data = {'title': ''}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_title()
        self.assertIn("El título no puede estar vacío", str(cm.exception))
    
    def test_clean_title_too_short(self):
        form = NotificationModelForm()
        form.cleaned_data = {'title': 'Hi'}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_title()
        self.assertIn("El título debe tener al menos 3 caracteres", str(cm.exception))
    
    def test_clean_message_valid(self):
        form = NotificationModelForm()
        form.cleaned_data = {'message': 'This is a valid message'}
        self.assertEqual(form.clean_message(), 'This is a valid message')
    
    def test_clean_message_empty(self):
        form = NotificationModelForm()
        form.cleaned_data = {'message': ''}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_message()
        self.assertIn("El mensaje no puede estar vacío", str(cm.exception))
    
    def test_clean_priority_valid(self):
        form = NotificationModelForm()
        form.cleaned_data = {'priority': 'alta'}
        self.assertEqual(form.clean_priority(), 'alta')
    
    def test_clean_priority_invalid(self):
        form = NotificationModelForm()
        form.cleaned_data = {'priority': 'urgente'}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_priority()
        self.assertIn("Prioridad no válida", str(cm.exception))


class RefundRequestFormTest(TestCase):
    
    def test_clean_ticket_code_valid(self):
        form = RefundRequestForm()
        form.cleaned_data = {'ticket_code': 'TKT123456'}
        self.assertEqual(form.clean_ticket_code(), 'TKT123456')
    
    def test_clean_ticket_code_empty(self):
        form = RefundRequestForm()
        form.cleaned_data = {'ticket_code': ''}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_ticket_code()
        self.assertIn("El código del ticket es obligatorio", str(cm.exception))
    
    def test_clean_reason_valid(self):
        form = RefundRequestForm()
        form.cleaned_data = {'reason': 'I cannot attend the event due to personal reasons'}
        self.assertEqual(form.clean_reason(), 'I cannot attend the event due to personal reasons')
    
    def test_clean_reason_empty(self):
        form = RefundRequestForm()
        form.cleaned_data = {'reason': ''}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_reason()
        self.assertIn("El motivo es obligatorio", str(cm.exception))
    
    def test_clean_reason_too_short(self):
        form = RefundRequestForm()
        form.cleaned_data = {'reason': 'Short'}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_reason()
        self.assertIn("El motivo debe tener al menos 10 caracteres", str(cm.exception))


class SignUpFormTest(TestCase):
    
    def setUp(self):
        # Create a test user to test email uniqueness
        User.objects.create_user(
            username='existing_user',
            email='existing@example.com',
            password='testpass123'
        )
    
    def test_clean_email_valid(self):
        form = SignUpForm()
        form.cleaned_data = {'email': 'new@example.com'}
        self.assertEqual(form.clean_email(), 'new@example.com')
    
    def test_clean_email_with_whitespace(self):
        form = SignUpForm()
        form.cleaned_data = {'email': '  new@example.com  '}
        self.assertEqual(form.clean_email(), 'new@example.com')
    
    def test_clean_email_duplicate(self):
        form = SignUpForm()
        form.cleaned_data = {'email': 'existing@example.com'}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_email()
        self.assertIn("Este correo electrónico ya está registrado", str(cm.exception))
    
    def test_clean_email_duplicate_case_insensitive(self):
        form = SignUpForm()
        form.cleaned_data = {'email': 'EXISTING@EXAMPLE.COM'}
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_email()
        self.assertIn("Este correo electrónico ya está registrado", str(cm.exception))