from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import(
    Comment,
    Rating,
    Venue,
    Category,
)

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['title', 'text', 'rating']


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)  # definir el campo fuera de Meta

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
                "class": "from_control",
                "placeholder": "Direccion",
            }),
            "city": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Ciudad",
            }),
            "capacity": forms.TextInput(attrs={
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
            "address": "Direccion",
            "capacity": "Capacidad",
            "contact": "Contacto", 
        }


    def clean_name(self):
        pass

    def clean_city(self):
        pass

    def clean_address(self):
        pass

    def clean_contact(self):
        pass


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