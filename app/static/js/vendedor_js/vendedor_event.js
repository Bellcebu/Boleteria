document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('eventForm');
    const formAction = document.getElementById('formAction');
    const eventId = document.getElementById('eventId');
    const submitBtn = document.getElementById('submitBtn');
    const cancelBtn = document.getElementById('cancelBtn');
    const cardHeader = document.querySelector('.card');
    const noEditMessage = document.getElementById('noEditMessage');

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

    document.querySelectorAll('.manage-tickets-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const eventId = this.dataset.eventId;
            window.location.href = `/admin-panel/eventos/${eventId}/tickets/`;
        });
    });

    if (cancelBtn) {
        cancelBtn.addEventListener('click', function() {
            resetForm();
        });
    }

    function loadEventForEdit(eventData) {
        formAction.value = 'edit';
        eventId.value = eventData.id;
       
        document.getElementById('id_title').value = eventData.title;
        document.getElementById('id_description').value = eventData.description;
        document.getElementById('id_date').value = eventData.date;
        document.getElementById('id_category').value = eventData.category;
        document.getElementById('id_venue_fk').value = eventData.venue;
       
        form.style.display = 'block';
        noEditMessage.style.display = 'none';
        cardHeader.classList.add('edit-mode');
       
        cardHeader.scrollIntoView({ behavior: 'smooth' });
    }

    function resetForm() {
        form.reset();
        form.style.display = 'none';
        noEditMessage.style.display = 'block';
        cardHeader.classList.remove('edit-mode');
    }
});