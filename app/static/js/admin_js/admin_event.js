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
                autor: this.dataset.autor,
                title: this.dataset.title,
                description: this.dataset.description,
                date: this.dataset.date,
                categories: this.dataset.categories ? this.dataset.categories.split(',') : [],
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
       
        document.getElementById('id_autor').value = eventData.autor || '';
        document.getElementById('id_title').value = eventData.title;
        document.getElementById('id_description').value = eventData.description;
        document.getElementById('id_date').value = eventData.date;
        document.querySelectorAll('input[name="category"]').forEach(checkbox => {
            checkbox.checked = eventData.categories.includes(checkbox.value);
        });
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
        document.querySelectorAll('input[name="category"]').forEach(checkbox => {
            checkbox.checked = false;
        });
       
        submitBtn.innerHTML = '<i class="bi bi-plus-circle me-2"></i>Crear Evento';
        cancelBtn.style.display = 'none';
        cardHeader.classList.remove('edit-mode');
    }
    
    const categoriesModal = document.getElementById('categoriesModal');
    if (categoriesModal) {
        categoriesModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const eventTitle = button.getAttribute('data-event-title');
            const categories = button.getAttribute('data-categories');
            
            document.getElementById('eventTitleModal').textContent = eventTitle;
            
            const container = document.getElementById('categoriesContainer');
            container.innerHTML = '';
            
            if (categories) {
                const categoryArray = categories.split(', ');
                categoryArray.forEach(category => {
                    const badge = document.createElement('span');
                    badge.className = 'badge bg-primary fs-6 px-3 py-2';
                    badge.textContent = category;
                    container.appendChild(badge);
                });
            } else {
                container.innerHTML = '<span class="text-muted">Este evento no tiene categorías asignadas</span>';
            }
        });
    }
});

document.querySelectorAll('.manage-tickets-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const eventId = this.dataset.eventId;
        window.location.href = `/admin_panel/eventos/${eventId}/tickets/`;
    });
});