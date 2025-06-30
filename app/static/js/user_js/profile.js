document.addEventListener('DOMContentLoaded', function() {
    // Auto-submit avatar form
    const avatarInput = document.getElementById('avatarInput');
    const avatarForm = document.getElementById('avatarForm');
   
    if (avatarInput && avatarForm) {
        avatarInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                avatarForm.submit();
            }
        });
    }
});

function openRefundModal(ticketId, eventTitle) {
    // Establecer valores en el modal
    document.getElementById('refundTicketId').value = ticketId;
    document.getElementById('eventTitle').value = eventTitle;
    document.getElementById('refundReason').value = '';
    
    // Abrir modal con Bootstrap 5
    const modal = new bootstrap.Modal(document.getElementById('refundModal'));
    modal.show();
}