from django.views.generic import TemplateView, ListView, View
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django import forms

from app.models import Event, RefundRequest


#accseso
class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff



class AdminDashboardView(StaffRequiredMixin, TemplateView):
    template_name = 'adminhtmls/home_admin.html'


class RefundListView(StaffRequiredMixin, ListView):
    model = RefundRequest
    template_name = 'admin_panel/refunds.html'
    context_object_name = 'refunds'

    def get_queryset(self):
        return RefundRequest.objects.order_by('-created_at')


class RefundActionView(StaffRequiredMixin, View):
    def post(self, request, pk, action):
        refund = get_object_or_404(RefundRequest, pk=pk)

        if action == 'approve':
            refund.approved = True
            refund.save()
            messages.success(request, f"Reembolso aprobado para ticket {refund.ticket_code}")
        elif action == 'reject':
            refund.delete()
            messages.info(request, f"Reembolso rechazado para ticket {refund.ticket_code}")

        return redirect('admin_reembolsos')



class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'category', 'venue_fk', 'base_price', 'image']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_base_price(self):
        price = self.cleaned_data.get('base_price')
        if price < 0:
            raise forms.ValidationError("El precio no puede ser negativo.")
        return price


class EventCreateView(StaffRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'adminhtmls/create_event.html'
    success_url = reverse_lazy('admin_dashboard')
