document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('promotionForm');
    const submitBtn = document.getElementById('submitBtn');
    const cancelBtn = document.getElementById('cancelBtn');
    const formAction = document.getElementById('formAction');
    const promotionId = document.getElementById('promotionId');
    
    document.getElementById('id_code').addEventListener('input', function() {
        this.value = this.value.toUpperCase();
    });
    
    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const data = this.dataset;
            
            form.closest('.card').classList.add('edit-mode');
            formAction.value = 'edit';
            promotionId.value = data.promotionId;
            
            document.getElementById('id_event').value = data.event;
            document.getElementById('id_code').value = data.code;
            document.getElementById('id_discount_percentage').value = data.discount;
            document.getElementById('id_start_date').value = data.start;
            document.getElementById('id_end_date').value = data.end;
            document.getElementById('id_max_uses').value = data.maxUses;
            document.getElementById('id_is_active').checked = data.active === 'True';
            
            submitBtn.innerHTML = '<i class="bi bi-save me-2"></i>Actualizar Promoción';
            cancelBtn.style.display = 'inline-block';
            
            form.scrollIntoView({ behavior: 'smooth' });
        });
    });
    
    cancelBtn.addEventListener('click', function() {
        form.reset();
        form.closest('.card').classList.remove('edit-mode');
        formAction.value = 'create';
        promotionId.value = '';
        
        submitBtn.innerHTML = '<i class="bi bi-save me-2"></i>Crear Promoción';
        cancelBtn.style.display = 'none';
    });
    
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const promotionId = this.dataset.promotionId;
            const code = this.dataset.code;
            const event = this.dataset.event;
            
            document.getElementById('deletePromotionId').value = promotionId;
            document.getElementById('promotionToDelete').textContent = code;
            document.getElementById('eventToDelete').textContent = event;
            
            const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
            deleteModal.show();
        });
    });
    
    document.getElementById('id_start_date').addEventListener('change', function() {
        const startDate = new Date(this.value);
        const endDateInput = document.getElementById('id_end_date');
        
        if (endDateInput.value) {
            const endDate = new Date(endDateInput.value);
            if (startDate >= endDate) {
                alert('La fecha de inicio debe ser anterior a la fecha de fin');
                this.value = '';
            }
        }
    });
    
    document.getElementById('id_end_date').addEventListener('change', function() {
        const endDate = new Date(this.value);
        const startDateInput = document.getElementById('id_start_date');
        
        if (startDateInput.value) {
            const startDate = new Date(startDateInput.value);
            if (endDate <= startDate) {
                alert('La fecha de fin debe ser posterior a la fecha de inicio');
                this.value = '';
            }
        }
    });
});