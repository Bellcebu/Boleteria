document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('categoryForm');
    const formAction = document.getElementById('formAction');
    const categoryId = document.getElementById('categoryId');
    const submitBtn = document.getElementById('submitBtn');
    const cancelBtn = document.getElementById('cancelBtn');
    const cardHeader = document.querySelector('.card');

    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const categoryData = {
                id: this.dataset.categoryId,
                name: this.dataset.name,
                description: this.dataset.description,
                is_active: this.dataset.isActive === 'True'
            };
            
            loadCategoryForEdit(categoryData);
        });
    });

    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.getElementById('categoryToDelete').textContent = this.dataset.name;
            document.getElementById('deleteCategoryId').value = this.dataset.categoryId;
            new bootstrap.Modal(document.getElementById('deleteModal')).show();
        });
    });

    cancelBtn.addEventListener('click', function() {
        resetForm();
    });

    function loadCategoryForEdit(categoryData) {
        formAction.value = 'edit';
        categoryId.value = categoryData.id;
        
        document.getElementById('id_name').value = categoryData.name;
        document.getElementById('id_description').value = categoryData.description;
        document.getElementById('id_is_active').checked = categoryData.is_active;
        
        submitBtn.innerHTML = '<i class="bi bi-save me-2"></i>Actualizar Categoría';
        cancelBtn.style.display = 'inline-block';
        cardHeader.classList.add('edit-mode');
        
        cardHeader.scrollIntoView({ behavior: 'smooth' });
    }

    function resetForm() {
        form.reset();
        formAction.value = 'create';
        categoryId.value = '';
        document.getElementById('id_is_active').checked = true;
        
        submitBtn.innerHTML = '<i class="bi bi-plus-circle me-2"></i>Crear Categoría';
        cancelBtn.style.display = 'none';
        cardHeader.classList.remove('edit-mode');
    }
});