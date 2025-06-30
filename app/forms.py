from django import forms
from django.db import models
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import (
    Event,
    TicketTier,
    Ticket,
    Comment,
    Rating,
    Venue,
    Category,
    Profile,
    Promotion,
    RefundRequest,
    Notification,
)


# --- Categorías ---
class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nombre",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Descripcion",
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check_input"
            }),
        }
        labels = {
            "name": "Nombre",
            "description": "Descripcion",
            "is_active": "Activo?",
        }

    def clean_name(self):
        name = self.cleaned_data.get("name", "") or ""
        name = name.strip()
        if not name:
            raise forms.ValidationError("El nombre no puede estar vacío.")
        if len(name) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description", "") or ""
        description = description.strip()
        if len(description) < 10:
            raise forms.ValidationError("La descripción debe tener al menos 10 caracteres.")
        return description

    def clean_is_active(self):
        return self.cleaned_data.get("is_active", True)


# --- Venues ---
class VenueModelForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'address', 'city', 'capacity', 'contact']
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nombre",
            }),
            "address": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Dirección",
            }),
            "city": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ciudad",
            }),
            "capacity": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Capacidad"
            }),
            "contact": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Contacto",
            }),
        }
        labels = {
            "name": "Nombre",
            "city": "Ciudad",
            "address": "Dirección",
            "capacity": "Capacidad",
            "contact": "Contacto",
        }

    def clean_name(self):
        name = self.cleaned_data.get("name", "") or ""
        name = name.strip()
        if len(name) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return name

    def clean_city(self):
        city = self.cleaned_data.get("city", "") or ""
        city = city.strip()
        if not city:
            raise forms.ValidationError("La ciudad es obligatoria.")
        if city.isnumeric():
            raise forms.ValidationError("La ciudad no puede ser un número.")
        return city

    def clean_address(self):
        address = self.cleaned_data.get("address", "") or ""
        address = address.strip()
        if len(address) < 5:
            raise forms.ValidationError("La dirección debe tener al menos 5 caracteres.")
        return address

    def clean_contact(self):
        contact = self.cleaned_data.get("contact", "") or ""
        contact = contact.strip()
        if len(contact) < 5:
            raise forms.ValidationError("El contacto debe tener al menos 5 caracteres.")
        return contact

    def clean_capacity(self):
        capacity = self.cleaned_data.get("capacity")
        if capacity is None or capacity <= 0:
            raise forms.ValidationError("La capacidad debe ser un número positivo.")
        return capacity


# --- Eventos ---
class EventModelForm(forms.ModelForm):
    date = forms.DateTimeField(widget = forms.DateTimeInput(attrs={'class':'form-control', 'type':'datetime-local'}, format='%Y-%m-%dT%H:%M'),input_formats=['%Y-%m-%dT%H:%M'])
    class Meta:
        model = Event
        fields = ['category', 'venue_fk', 'autor' , 'title', 'description', 'date', 'image']
        widgets = {
            'category':forms.CheckboxSelectMultiple(),
            'venue_fk': forms.Select(attrs={
                'class': 'form-control'
                }),
            'autor': forms.TextInput(attrs={ 
                'class': 'form-control',
                'placeholder': 'Autor (opcional)'
                }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del evento'
                }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 5, 'placeholder': 'Descripción'
                }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
                }),
        }
        labels = {
            'category': 'Categoría',
            'venue_fk': 'Lugar',
            'autor': 'Autor', 
            'title': 'Título',
            'description': 'Descripción',
            'date': 'Fecha y hora',
            'image': 'Imagen del evento',
        }

    def clean_title(self):
        title = self.cleaned_data.get("title", "") or ""
        title = title.strip()
        if not title:
            raise forms.ValidationError("El título es obligatorio.")
        if len(title) < 5:
            raise forms.ValidationError("El título debe tener al menos 5 caracteres.")
        return title

    def clean_description(self):
        description = self.cleaned_data.get("description", "") or ""
        description = description.strip()
        if not description:
            raise forms.ValidationError("La descripción es obligatoria.")
        if len(description) < 20:
            raise forms.ValidationError("La descripción debe tener al menos 20 caracteres.")
        return description

    def clean_date(self):
        date = self.cleaned_data.get("date")
        if not date:
            raise forms.ValidationError("La fecha es obligatoria.")
        return date


# --- Tickets ---
class TicketPurchaseForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        label="Cantidad",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad de entradas'})
    )

    def __init__(self, *args, **kwargs):
        self.ticket_tier = kwargs.pop('ticket_tier', None)
        super().__init__(*args, **kwargs)

    def clean_quantity(self):
        qty = self.cleaned_data['quantity']
        if self.ticket_tier:
            from django.db.models import Sum
            from .models import Ticket
            sold_qty = Ticket.objects.filter(
                ticket_tier=self.ticket_tier
            ).aggregate(
                total=Sum('quantity')
            )['total'] or 0
            max_qty = self.ticket_tier.max_quantity or 0
            available_qty = max_qty - sold_qty
            
            if available_qty < qty:
                raise forms.ValidationError(
                    f"Solo quedan {available_qty} entradas disponibles para esta categoría."
                )
        return qty


class TicketModelForm(forms.ModelForm):
    class Meta:
        model = TicketTier
        fields = ['name', 'price', 'description', 'max_quantity', 'is_available']
        widgets = {
            'name': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Nombre del ticket',
                }),
            'price': forms.NumberInput(attrs={
                'class':'form-control',
                'min':'0','step':'0.01'
                }),
            'description': forms.Textarea(attrs={
                'class':'form-control',
                'rows':2,
                'placeholder':'Descripción opcional'
                }),
            'max_quantity': forms.NumberInput(attrs={
                'class':'form-control',
                'min':'1'
                }),
            'is_available': forms.CheckboxInput(attrs={
                'class':'form-check-input'
                }),
        }
        labels = {
            'name': 'Nombre de la entrada',
            'price': 'Precio',
            'description': 'Descripción',
            'max_quantity': 'Cantidad máxima',
            'is_available': 'Disponible',
        }

    def clean_name(self):
        name = self.cleaned_data.get("name", "") or ""
        name = name.strip()
        if not name:
            raise forms.ValidationError("El nombre es obligatorio.")
        return name

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is None or price < 0:
            raise forms.ValidationError("El precio debe ser mayor o igual a 0.")
        return price

    def clean_max_quantity(self):
        max_quantity = self.cleaned_data.get("max_quantity")
        if max_quantity is None or max_quantity <= 0:
            raise forms.ValidationError("La cantidad máxima debe ser mayor que 0.")
        return max_quantity


class TicketTierInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        total_qty = 0
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                qty = form.cleaned_data.get('max_quantity') or 0
                total_qty += qty

        venue = self.instance.venue_fk
        if venue and total_qty > venue.capacity:
            raise ValidationError(
                f"La suma de cantidades ({total_qty}) excede la capacidad del venue ({venue.capacity})."
            )


TicketTierFormSet = inlineformset_factory(
    Event,
    TicketTier,
    form=TicketModelForm,
    formset=TicketTierInlineFormSet,
    extra=1,
    can_delete=True,
)


# --- Promociones ---
class PromotionForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class':'form-control',
            'type':'datetime-local',
            }),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class':'form-control', 'type':'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    
    class Meta:
        model = Promotion
        fields = ['code', 'discount_percentage', 'start_date', 'end_date', 'max_uses']
        widgets = {
            'code': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Código promocional',
                }),
            'discount_percentage': forms.NumberInput(attrs={
                'class':'form-control',
                'min':'0',
                'max':'100',
                }),
            'max_uses': forms.NumberInput(attrs={
                'class':'form-control',
                'min':'1'
                }),
        }
        labels = {
            'code': 'Código',
            'discount_percentage': 'Porcentaje de descuento',
            'start_date': 'Fecha de inicio',
            'end_date': 'Fecha de fin',
            'max_uses': 'Usos máximos',
        }

    def clean_code(self):
        code = self.cleaned_data.get("code", "") or ""
        code = code.strip().upper()
        if not code:
            raise forms.ValidationError("El código es obligatorio.")
        if len(code) < 3:
            raise forms.ValidationError("El código debe tener al menos 3 caracteres.")
        return code

    def clean_discount_percentage(self):
        discount = self.cleaned_data.get("discount_percentage")
        if discount is None or not (0 < discount <= 100):
            raise forms.ValidationError("El descuento debe estar entre 0.01 y 100.")
        return discount

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError('La fecha de inicio debe ser anterior a la fecha de fin.')
        
        return cleaned_data


# --- Ratings ---
class RatingModelForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['title', 'text', 'rating']
        widgets = {
            'title': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Título de tu calificación'
                }),
            'text': forms.Textarea(attrs={
                'class':'form-control',
                'rows':3,
                'placeholder':'Comparte tu experiencia',
                }),
            'rating': forms.NumberInput(attrs={
                'class':'form-control',
                'min':'1',
                'max':'5',
                }),
        }
        labels = {
            'title': 'Título',
            'text': 'Comentario',
            'rating': 'Calificación',
        }

    def clean_title(self):
        title = self.cleaned_data.get("title", "") or ""
        title = title.strip()
        if not title:
            raise forms.ValidationError("El título es obligatorio.")
        return title

    def clean_text(self):
        text = self.cleaned_data.get("text", "") or ""
        text = text.strip()
        if not text:
            raise forms.ValidationError("El comentario es obligatorio.")
        return text

    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        if rating is None or not (1 <= rating <= 5):
            raise forms.ValidationError("La calificación debe estar entre 1 y 5.")
        return rating


# --- Comentarios ---
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'text']
        widgets = {
            'title': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Título del comentario'
                }),
            'text': forms.Textarea(attrs={
                'class':'form-control',
                'rows':3,
                'placeholder':'Escribe tu comentario'
                }),
        }
        labels = {
            'title': 'Título',
            'text': 'Comentario',
        }

    def clean_title(self):
        title = self.cleaned_data.get("title", "") or ""
        title = title.strip()
        if not title:
            raise forms.ValidationError("El título es obligatorio.")
        return title

    def clean_text(self):
        text = self.cleaned_data.get("text", "") or ""
        text = text.strip()
        if not text:
            raise forms.ValidationError("El comentario es obligatorio.")
        return text


class NotificationModelForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['title', 'message', 'priority', 'is_read', 'users']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título de la notificación',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Mensaje de la notificación',
            }),
            'priority': forms.Select(attrs={
                'class': 'form-control',
            }),
            'is_read': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'users': forms.SelectMultiple(attrs={
                'class': 'form-select',
            }),
        }

        labels = {
            'title': 'Título',
            'message': 'Mensaje',
            'priority': 'Prioridad',
            'is_read': '¿Leída?',
            'users': 'Usuarios destinatarios',
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise forms.ValidationError("El título no puede estar vacío.")
        if len(title) < 3:
            raise forms.ValidationError("El título debe tener al menos 3 caracteres.")
        return title

    def clean_message(self):
        message = self.cleaned_data.get('message', '').strip()
        if not message:
            raise forms.ValidationError("El mensaje no puede estar vacío.")
        return message

    def clean_priority(self):
        priority = self.cleaned_data.get('priority')
        valid_choices = ['alta', 'media', 'baja']
        if priority not in valid_choices:
            raise forms.ValidationError("Prioridad no válida.")
        return priority

# --- Reembolsos ---
class RefundRequestForm(forms.ModelForm):
    class Meta:
        model = RefundRequest
        fields = ['ticket_code', 'reason']
        widgets = {
            'ticket_code': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Código del ticket',
                }),
            'reason': forms.Textarea(attrs={
                'class':'form-control',
                'rows':3,
                'placeholder':'Motivo del reembolso',
                }),
        }
        labels = {
            'ticket_code': 'Código del ticket',
            'reason': 'Motivo',
        }

    def clean_ticket_code(self):
        ticket_code = self.cleaned_data.get("ticket_code", "") or ""
        ticket_code = ticket_code.strip()
        if not ticket_code:
            raise forms.ValidationError("El código del ticket es obligatorio.")
        return ticket_code

    def clean_reason(self):
        reason = self.cleaned_data.get("reason", "") or ""
        reason = reason.strip()
        if not reason:
            raise forms.ValidationError("El motivo es obligatorio.")
        if len(reason) < 10:
            raise forms.ValidationError("El motivo debe tener al menos 10 caracteres.")
        return reason


# --- Autenticación ---
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Correo electrónico',
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contraseña'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmar contraseña'})

    def clean_email(self):
        email = self.cleaned_data.get('email', '') or ''
        email = email.strip()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email


# --- Perfil ---
class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'avatar': 'Foto de perfil',
        }