from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import (
    Comment,
    Rating,
    Venue,
    Category,
    Ticket,
    TicketTier,
    Promotion,
    Event,
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
        name = self.cleaned_data.get("name", "").strip()
        if not name:
            raise forms.ValidationError("El nombre no puede estar vacío.")
        if len(name) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description", "").strip()
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
        name = self.cleaned_data.get("name", "").strip()
        if len(name) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return name

    def clean_city(self):
        city = self.cleaned_data.get("city", "").strip()
        if not city:
            raise forms.ValidationError("La ciudad es obligatoria.")
        if city.isnumeric():
            raise forms.ValidationError("La ciudad no puede ser un número.")
        return city

    def clean_address(self):
        address = self.cleaned_data.get("address", "").strip()
        if len(address) < 5:
            raise forms.ValidationError("La dirección debe tener al menos 5 caracteres.")
        return address

    def clean_contact(self):
        contact = self.cleaned_data.get("contact", "").strip()
        if len(contact) < 5:
            raise forms.ValidationError("El contacto debe tener al menos 5 caracteres.")
        return contact


class EventModelForm(forms.ModelForm):
    # Campos adicionales para los precios de tickets
    general_price = forms.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
        label='Precio Entrada General'
    )
    premium_price = forms.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
        label='Precio Entrada Premium (Opcional)'
    )
    vip_price = forms.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
        label='Precio Entrada VIP (Opcional)'
    )
    ultra_vip_price = forms.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
        label='Precio Entrada Ultra VIP (Opcional)'
    )

    class Meta:
        model = Event
        fields = ['category', 'venue_fk', 'title', 'description', 'date', 'image', 'base_price']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'venue_fk': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del evento'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Descripción'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'base_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'category': 'Categoría',
            'venue_fk': 'Lugar',
            'title': 'Título',
            'description': 'Descripción',
            'date': 'Fecha y hora',
            'image': 'Imagen del evento',
            'base_price': 'Precio base',
        }

    def clean_title(self):
        title = self.cleaned_data.get("title", "").strip()
        if len(title) < 5:
            raise forms.ValidationError("El título debe tener al menos 5 caracteres.")
        return title

    def clean_description(self):
        description = self.cleaned_data.get("description", "").strip()
        if len(description) < 20:
            raise forms.ValidationError("La descripción debe tener al menos 20 caracteres.")
        return description

    def clean_base_price(self):
        base_price = self.cleaned_data.get("base_price")
        if base_price < 0:
            raise forms.ValidationError("El precio no puede ser negativo.")
        return base_price

    def clean_general_price(self):
        general_price = self.cleaned_data.get("general_price")
        if general_price < 0:
            raise forms.ValidationError("El precio general no puede ser negativo.")
        return general_price

    def clean(self):
        cleaned_data = super().clean()
        general_price = cleaned_data.get('general_price')
        premium_price = cleaned_data.get('premium_price')
        vip_price = cleaned_data.get('vip_price')
        ultra_vip_price = cleaned_data.get('ultra_vip_price')
        
        # Validar que los precios estén en orden ascendente
        prices = []
        if general_price is not None:
            prices.append(('General', general_price))
        if premium_price is not None:
            prices.append(('Premium', premium_price))
        if vip_price is not None:
            prices.append(('VIP', vip_price))
        if ultra_vip_price is not None:
            prices.append(('Ultra VIP', ultra_vip_price))
        
        # Verificar orden
        for i in range(1, len(prices)):
            if prices[i][1] <= prices[i-1][1]:
                raise forms.ValidationError(
                    f"El precio {prices[i][0]} debe ser mayor que {prices[i-1][0]}"
                )
        
        return cleaned_data

class TicketModelForm(forms.ModelForm):
    class Meta:
        model = TicketTier
        fields = ['name', 'price', 'description', 'max_quantity']
        widgets = {
            "quantity": forms.NumberInput(attrs={
                "class": "form-control"
            }),
            "type": forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            "quantity": "Cantidad",
            "type": "Tipo",
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity")
        if quantity is None or quantity <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor que 0.")
        return quantity

    def clean_type(self):
        ticket_type = self.cleaned_data.get("type")
        valid_types = [choice[0] for choice in Ticket.TicketType.choices]
        if ticket_type not in valid_types:
            raise forms.ValidationError(f"Tipo inválido. Debe ser uno de {valid_types}.")
        return ticket_type
    
class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = ['code', 'discount_percentage', 'start_date', 'end_date', 'max_uses']


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['title', 'text', 'rating']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'text']


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
