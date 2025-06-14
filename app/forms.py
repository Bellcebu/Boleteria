from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import(
    Comment,
    Rating,
    Venue,
    Category,
    Ticket,
    Event,
)

class EventModelForm(forms.ModelForm):
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

class TicketModelForm(forms.ModelForm):
    class Meta:
        model=Ticket
        fields=["quantity","type"]
        widgets = {
            "quantity":forms.NumberInput(attrs={
                "class" : "from-control"
            }),
            "type": forms.Select(attrs={
                'class': 'form-control'
            }),
        }

        labels={
            "quantity":"cantidad",
            "type":"tipo",
        }

    def clean_quantity(self):
        pass
    def clean_type(self):
        pass

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['title', 'text', 'rating']


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)  

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'text']


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


class CategoryModelForm(forms.ModelForm):
    class Meta: 
        model = Category
        fields = ["name", "description", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs= {
                "class": "form-control",
                "placeholder": "Nombre",
            }),
            "description": forms.Textarea(attrs= {
                "class": "form-control",
                "placeholder": "Descripcion",
            }),
            "is_active": forms.CheckboxInput(attrs= {
                "class": "form-check_input"
            }),
        }

        labels={
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