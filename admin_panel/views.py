from django.views.generic import ListView, View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import TemplateView
from app.models import RefundRequest 

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
