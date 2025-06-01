from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import check_password,make_password
from .models import (
    Event,
    Ticket,
)
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth import login,logout
from .forms import SignUpForm

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


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        return render(request, 'login.html', {'form': form})
    
class LogOutView(View):
    def get(self,request):
        logout(request)
        return redirect('login')
        
class SignUpView(View):
    def get(self,request):
        form = SignUpForm
        return(render,'signup.html',{'form':form})

    def post(self,request):
        form = SignUpForm(request.POST)
        if form.is_valid:
            user = form.save()
            login(request,user)
            redirect('home.html')
        return(render,'signup.html',{'form':form})
    
class ticketListView(LoginRequiredMixin,ListView):
    model = Ticket
    template = "tickets.html"
    context = "tickets"

    def get_queryset(self):
        return Ticket.objects.filter(user_fk=self.request.user).order_by("-buy_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def post(self,request,*args,**kwargs):
        ticket_id=request.POST.get('ticket_id')

        if ticket_id:
            ticket = Ticket.objects.filter(ticket_code=ticket_id, user_fk=request.user).first
            if ticket:
                ticket.refound_request=True
                ticket.save() 
        return redirect(request,'tickets.html')

