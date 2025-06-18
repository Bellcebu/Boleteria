document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const dateInput = document.getElementById('id_date');

    if (dateInput) {
        dateInput.addEventListener('change', function() {
            const selectedDate = new Date(this.value);
            const now = new Date();

            if (selectedDate < now) {
                alert('La fecha del evento no puede ser en el pasado.');
                this.focus();
            }
        });
    }

    form.addEventListener('submit', function(e) {
        if (!confirm('¿Estás seguro de que quieres guardar los cambios?')) {
            e.preventDefault();
        }
    });
});
