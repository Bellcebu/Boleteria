// Confirmación de eliminación: asigna ruta y CSRF
function confirmDelete(eventId, eventTitle) {
    const modal      = document.getElementById('deleteModal');
    const titleSpan  = document.getElementById('eventTitle');
    const deleteForm = document.getElementById('deleteForm');
  
    // Acción apunta al DeleteView en admin_panel
    deleteForm.action = `/admin-panel/events/${eventId}/borrar/`;
  
    // Inserta token CSRF y botón de confirmación
    deleteForm.innerHTML = `
      <input type="hidden" name="csrfmiddlewaretoken" value="${getCookie('csrftoken')}">
      <button type="submit" class="action-btn confirm-delete">
        <i class="fas fa-trash"></i> Sí, eliminar
      </button>
    `;
  
    titleSpan.textContent = eventTitle;
    modal.style.display = 'flex';
  }
  
  // Cierra el modal
  function closeDeleteModal() {
    document.getElementById('deleteModal').style.display = 'none';
  }
  
  // Lectura de cookie CSRF
  function getCookie(name) {
    let value = null;
    document.cookie.split(';').forEach(cookie => {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        value = decodeURIComponent(cookie.slice(name.length + 1));
      }
    });
    return value;
  }
  
  // Cerrar modal al click fuera
  window.onclick = e => {
    const modal = document.getElementById('deleteModal');
    if (e.target === modal) closeDeleteModal();
  };