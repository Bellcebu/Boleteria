document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('ticketForm');
    const formAction = document.getElementById('formAction');
    const ticketId = document.getElementById('ticketId');
    const submitBtn = document.getElementById('submitBtn');
    const cancelBtn = document.getElementById('cancelBtn');
    const cardHeader = document.querySelector('.card');

    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const ticketData = {
                id: this.dataset.ticketId,
                name: this.dataset.name,
                price: this.dataset.price,
                max_quantity: this.dataset.maxQuantity,
                description: this.dataset.description,
                is_available: this.dataset.isAvailable === 'True'
            };
            
            loadTicketForEdit(ticketData);
        });
    });

    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.getElementById('ticketToDelete').textContent = this.dataset.name;
            document.getElementById('deleteTicketId').value = this.dataset.ticketId;
            new bootstrap.Modal(document.getElementById('deleteModal')).show();
        });
    });

    cancelBtn.addEventListener('click', function() {
        resetForm();
    });

    function loadTicketForEdit(ticketData) {
        formAction.value = 'edit';
        ticketId.value = ticketData.id;
        
        document.getElementById('id_name').value = ticketData.name;
        document.getElementById('id_price').value = ticketData.price;
        document.getElementById('id_max_quantity').value = ticketData.max_quantity;
        document.getElementById('id_description').value = ticketData.description;
        document.getElementById('id_is_available').checked = ticketData.is_available;
        
        submitBtn.innerHTML = '<i class="bi bi-save me-2"></i>Actualizar Ticket';
        cancelBtn.style.display = 'inline-block';
        cardHeader.classList.add('edit-mode');
        
        cardHeader.scrollIntoView({ behavior: 'smooth' });
    }

    function resetForm() {
        form.reset();
        formAction.value = 'create';
        ticketId.value = '';
        document.getElementById('id_is_available').checked = true;
        
        submitBtn.innerHTML = '<i class="bi bi-plus-circle me-2"></i>Crear Ticket';
        cancelBtn.style.display = 'none';
        cardHeader.classList.remove('edit-mode');
    }
});