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
)


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


class EventModelForm(forms.ModelForm):
    date = forms.DateTimeField(widget = forms.DateTimeInput(attrs={'class':'form-control', 'type':'datetime-local'}, format='%Y-%m-%dT%H:%M'),input_formats=['%Y-%m-%dT%H:%M'])
    class Meta:
        model = Event
        fields = ['category', 'venue_fk', 'title', 'description', 'date', 'image']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'venue_fk': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del evento'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Descripción'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'category': 'Categoría',
            'venue_fk': 'Lugar',
            'title': 'Título',
            'description': 'Descripción',
            'date': 'Fecha y hora',
            'image': 'Imagen del evento',
        }

    def clean_title(self):
        title = self.cleaned_data.get("title", "") or ""
        title = title.strip()
        if len(title) < 5:
            raise forms.ValidationError("El título debe tener al menos 5 caracteres.")
        return title

    def clean_description(self):
        description = self.cleaned_data.get("description", "") or ""
        description = description.strip()
        if len(description) < 20:
            raise forms.ValidationError("La descripción debe tener al menos 20 caracteres.")
        return description

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
            print(f"TicketTier: {self.ticket_tier.name}")
            print(f"Max quantity: {max_qty}")
            print(f"Sold quantity: {sold_qty}")
            print(f"Available quantity: {available_qty}")
            print(f"Requested quantity: {qty}")
            
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
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre del ticket'}),
            'price': forms.NumberInput(attrs={'class':'form-control','min':'0','step':'0.01'}),
            'description': forms.Textarea(attrs={'class':'form-control','rows':2,'placeholder':'Descripción opcional'}),
            'max_quantity': forms.NumberInput(attrs={'class':'form-control','min':'1'}),
            'is_available': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }
        labels = {
            'name': 'Nombre de la entrada',
            'price': 'Precio',
            'description': 'Descripción',
            'max_quantity': 'Cantidad máxima',
            'is_available': 'Disponible',
        }

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


class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = ['code', 'discount_percentage', 'start_date', 'end_date', 'max_uses']
        widgets = {
            'code': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Código promocional'}),
            'discount_percentage': forms.NumberInput(attrs={'class':'form-control', 'min':'0', 'max':'100'}),
            'start_date': forms.DateTimeInput(attrs={'class':'form-control', 'type':'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class':'form-control', 'type':'datetime-local'}),
            'max_uses': forms.NumberInput(attrs={'class':'form-control', 'min':'1'}),
        }
        labels = {
            'code': 'Código',
            'discount_percentage': 'Porcentaje de descuento',
            'start_date': 'Fecha de inicio',
            'end_date': 'Fecha de fin',
            'max_uses': 'Usos máximos',
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['title', 'text', 'rating']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'text': forms.Textarea(attrs={'class':'form-control', 'rows':3}),
            'rating': forms.NumberInput(attrs={'class':'form-control', 'min':'1', 'max':'5'}),
        }
        labels = {
            'title': 'Título',
            'text': 'Comentario',
            'rating': 'Calificación',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'text']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'text': forms.Textarea(attrs={'class':'form-control', 'rows':3}),
        }
        labels = {
            'title': 'Título',
            'text': 'Comentario',
        }


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
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '') or ''
        email = email.strip()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']

