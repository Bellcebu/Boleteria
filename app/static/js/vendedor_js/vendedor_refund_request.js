document.addEventListener('DOMContentLoaded', function() {
    
    document.querySelectorAll('.view-reason-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.getElementById('reasonUser').textContent = this.dataset.user;
            document.getElementById('reasonText').textContent = this.dataset.reason;
            new bootstrap.Modal(document.getElementById('reasonModal')).show();
        });
    });

    document.querySelectorAll('.approve-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.getElementById('approveUser').textContent = this.dataset.user;
            document.getElementById('approveTicket').textContent = '#' + this.dataset.ticket;
            document.getElementById('approveRefundId').value = this.dataset.refundId;
            new bootstrap.Modal(document.getElementById('approveModal')).show();
        });
    });

    document.querySelectorAll('.reject-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.getElementById('rejectUser').textContent = this.dataset.user;
            document.getElementById('rejectTicket').textContent = '#' + this.dataset.ticket;
            document.getElementById('rejectRefundId').value = this.dataset.refundId;
            new bootstrap.Modal(document.getElementById('rejectModal')).show();
        });
    });
});