// event_list.js

function confirmDelete(eventId, eventTitle) {
    const modal = document.getElementById('deleteModal');
    const titleSpan = document.getElementById('eventTitle');
    const deleteForm = document.getElementById('deleteForm');
    
    // Configurar el modal
    titleSpan.textContent = eventTitle;
    deleteForm.innerHTML = `
        <input type="hidden" name="csrfmiddlewaretoken" value="${getCookie('csrftoken')}">
        <input type="hidden" name="event_id" value="${eventId}">
        <button type="submit" class="action-btn confirm-delete">
            <i class="fas fa-trash"></i> Sí, eliminar
        </button>
    `;
    
    // Mostrar el modal
    modal.style.display = 'flex';
}

function closeDeleteModal() {
    const modal = document.getElementById('deleteModal');
    modal.style.display = 'none';
}

// Función para obtener el token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Cerrar modal al hacer clic fuera de él
window.onclick = function(event) {
    const modal = document.getElementById('deleteModal');
    if (event.target === modal) {
        closeDeleteModal();
    }
}