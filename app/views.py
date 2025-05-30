from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password,make_password
from .models import User
from .models import Event
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.models import AnonymousUser
import re


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        return context


class EventListView(ListView):
    model = Event
    template_name = "app/events.html"
    context_object_name = "events"

    def get_queryset(self):
        return Event.objects.all().order_by("date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = "app/event_detail.html"
    context_object_name = "event"

class SignUpView(View):
    def get(self, request):
        return render(request, 'signup.html')

    
    def post(self, request):
        def is_password_secure(password):
        # Regex explanation:
        # (?=.*[A-Z])  → at least one uppercase letter
        # (?=.*\d)     → at least one digit
        # .{8,}        → at least 8 characters long (you can change this)
            pattern = r'^(?=.*[A-Z])(?=.*\d).{8,}$'
            return bool(re.match(pattern, password))
        
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
        elif not is_password_secure(password):   
            messages.error = "Password must be at least 8 characters long, contain an uppercase letter and a number."
        else:
            hashed_password = make_password(password)
            User.objects.create(username=username, email=email, password=hashed_password)
            messages.success(request, "Account created. Please log in.")
            return redirect('login')

        return render(request, 'signup.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')

        user = User.objects.filter(username=identifier).first() or User.objects.filter(email=identifier).first()

        if user and check_password(password, user.password):
            login(request, user) 
            return redirect('home')
        else:
            messages.error(request, 'Invalid username/email or password')
            return render(request, 'login.html')