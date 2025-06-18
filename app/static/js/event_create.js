document.addEventListener('DOMContentLoaded', function() {
    const addTicketBtn = document.getElementById('add-ticket-btn');
    const ticketsContainer = document.getElementById('tickets-container');
    const totalFormsInput = document.querySelector('input[name$="-TOTAL_FORMS"]');

    if (!addTicketBtn || !ticketsContainer || !totalFormsInput) {
        console.error('Elementos del formset de tickets no encontrados');
        return;
    }

    function getPrefix() {
        return totalFormsInput.name.replace('-TOTAL_FORMS', '');
    }

    function updateIndices(form, index) {
        const prefix = getPrefix();
        form.querySelectorAll('input, select, textarea, label').forEach(el => {
            ['name', 'id', 'for'].forEach(attr => {
                if (el.hasAttribute(attr)) {
                    el.setAttribute(attr, el.getAttribute(attr).replace(new RegExp(`${prefix}-(\\d+)-`, 'g'), `${prefix}-${index}-`));
                }
            });
        });
        form.setAttribute('data-form-index', index);
        const title = form.querySelector('h6');
        if (title) title.innerHTML = `<i class="fas fa-ticket-alt me-1"></i>Ticket #${index + 1}`;
    }

    function clearValues(form) {
        form.querySelectorAll('input[type="text"], input[type="number"], textarea').forEach(input => input.value = '');
        form.querySelectorAll('select').forEach(select => select.selectedIndex = 0);
        form.querySelectorAll('input[type="checkbox"]').forEach(checkbox => checkbox.checked = checkbox.name.includes('is_available'));
        form.querySelectorAll('.text-danger').forEach(err => err.remove());
    }

    function reindexAll() {
        const forms = Array.from(ticketsContainer.querySelectorAll('.ticket-form'))
            .filter(f => f.style.display !== 'none');
        forms.forEach((form, idx) => updateIndices(form, idx));
        totalFormsInput.value = forms.length;
    }

    addTicketBtn.addEventListener('click', function() {
        const currentCount = parseInt(totalFormsInput.value, 10);
        const templateForm = ticketsContainer.querySelector('.ticket-form');
        const newForm = templateForm.cloneNode(true);
        clearValues(newForm);
        updateIndices(newForm, currentCount);
        const header = newForm.querySelector('.d-flex.justify-content-between');
        if (!header.querySelector('.remove-ticket-btn')) {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'btn btn-outline-danger btn-sm remove-ticket-btn';
            btn.innerHTML = '<i class="fas fa-trash me-1"></i>Eliminar';
            btn.addEventListener('click', () => removeForm(newForm));
            header.appendChild(btn);
        }
        ticketsContainer.appendChild(newForm);
        totalFormsInput.value = currentCount + 1;
    });

    function removeForm(form) {
        const deleteInput = form.querySelector(`input[name$='-DELETE']`);
        if (deleteInput) {
            deleteInput.checked = true;
            form.style.display = 'none';
        } else {
            form.remove();
        }
        reindexAll();
    }

    ticketsContainer.addEventListener('click', function(e) {
        if (e.target.closest('.remove-ticket-btn')) {
            const form = e.target.closest('.ticket-form');
            removeForm(form);
        }
    });
});
