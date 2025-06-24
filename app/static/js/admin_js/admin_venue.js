document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('venueForm');
    const formAction = document.getElementById('formAction');
    const venueId = document.getElementById('venueId');
    const submitBtn = document.getElementById('submitBtn');
    const cancelBtn = document.getElementById('cancelBtn');
    const cardHeader = document.querySelector('.card');

    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const venueData = {
                id: this.dataset.venueId,
                name: this.dataset.name,
                city: this.dataset.city,
                address: this.dataset.address,
                capacity: this.dataset.capacity,
                contact: this.dataset.contact
            };
            
            loadVenueForEdit(venueData);
        });
    });

    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.getElementById('venueToDelete').textContent = this.dataset.name;
            document.getElementById('deleteVenueId').value = this.dataset.venueId;
            new bootstrap.Modal(document.getElementById('deleteModal')).show();
        });
    });

    cancelBtn.addEventListener('click', function() {
        resetForm();
    });

    function loadVenueForEdit(venueData) {
        formAction.value = 'edit';
        venueId.value = venueData.id;
        
        document.getElementById('id_name').value = venueData.name;
        document.getElementById('id_city').value = venueData.city;
        document.getElementById('id_address').value = venueData.address;
        document.getElementById('id_capacity').value = venueData.capacity;
        document.getElementById('id_contact').value = venueData.contact;
        
        submitBtn.innerHTML = '<i class="bi bi-save me-2"></i>Actualizar Lugar';
        cancelBtn.style.display = 'inline-block';
        cardHeader.classList.add('edit-mode');
        
        cardHeader.scrollIntoView({ behavior: 'smooth' });
    }

    function resetForm() {
        form.reset();
        formAction.value = 'create';
        venueId.value = '';
        
        submitBtn.innerHTML = '<i class="bi bi-plus-circle me-2"></i>Crear Lugar';
        cancelBtn.style.display = 'none';
        cardHeader.classList.remove('edit-mode');
    }
});