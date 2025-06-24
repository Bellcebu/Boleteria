document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('eventForm');
    const formAction = document.getElementById('formAction');
    const eventId = document.getElementById('eventId');
    const submitBtn = document.getElementById('submitBtn');
    const cancelBtn = document.getElementById('cancelBtn');
    const cardHeader = document.querySelector('.card');

    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventData = {
                id: this.dataset.eventId,
                title: this.dataset.title,
                description: this.dataset.description,
                date: this.dataset.date,
                category: this.dataset.category,
                venue: this.dataset.venue
            };
            
            loadEventForEdit(eventData);
        });
    });

    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.getElementById('eventToDelete').textContent = this.dataset.title;
            document.getElementById('deleteEventId').value = this.dataset.eventId;
            new bootstrap.Modal(document.getElementById('deleteModal')).show();
        });
    });

    cancelBtn.addEventListener('click', function() {
        resetForm();
    });

    function loadEventForEdit(eventData) {
        formAction.value = 'edit';
        eventId.value = eventData.id;
        
        document.getElementById('id_title').value = eventData.title;
        document.getElementById('id_description').value = eventData.description;
        document.getElementById('id_date').value = eventData.date;
        document.getElementById('id_category').value = eventData.category;
        document.getElementById('id_venue_fk').value = eventData.venue;
        
        submitBtn.innerHTML = '<i class="bi bi-save me-2"></i>Actualizar Evento';
        cancelBtn.style.display = 'inline-block';
        cardHeader.classList.add('edit-mode');
        
        cardHeader.scrollIntoView({ behavior: 'smooth' });
    }

    function resetForm() {
        form.reset();
        formAction.value = 'create';
        eventId.value = '';
        
        submitBtn.innerHTML = '<i class="bi bi-plus-circle me-2"></i>Crear Evento';
        cancelBtn.style.display = 'none';
        cardHeader.classList.remove('edit-mode');
    }
});

document.querySelectorAll('.manage-tickets-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const eventId = this.dataset.eventId;
        window.location.href = `/admin_panel/eventos/${eventId}/tickets/`;
    });
});