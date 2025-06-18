function toggleRefundForm(ticketId) {
    const form = document.getElementById('refund-form-' + ticketId);
    if (form.classList.contains('show')) {
      form.classList.remove('show');
    } else {
      const allForms = document.querySelectorAll('.refund-form.show');
      allForms.forEach(f => f.classList.remove('show'));
      form.classList.add('show');
    }
  }