from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from models import(
    Comment,
    Rating,
)

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['title','text','rating']

class SignUpForm(UserCreationForm):

    class Meta:
        email = forms.EmailField(required=True)

        model=User
        fields = ['username','email','password1','password2']

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields = ['title', 'text']
